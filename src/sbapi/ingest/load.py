"""
Scrape records -> Postgres. Idempotent: running it twice on the same records
leaves the database as one run does.

    Pass 1  upsert each entity's own columns, keyed by source_url (the wiki page).
    Pass 2  resolve names to ids: foreign keys, then relationship rows.
    Pass 3  annotations (trivia, citations) and quotes.

Rows a record owns (its trivia, citations, appears_in, crew, cast) are deleted
and re-inserted for that entity, so edits on the wiki replace stale rows.
Names that match no record are left null and reported, never guessed. The one
exception is actors: a character page naming its actor is enough to create an
actor row with just that name.

Everything runs in one transaction: a failed load changes nothing.
"""

import urllib.parse
from collections import defaultdict
from dataclasses import dataclass, field

import psycopg

# entity type -> (table, name column, scalar columns copied as-is from the record)
TABLES = {
    "media": ("media", "title", ["media_type", "release_date", "description", "image_url"]),
    "actor": ("actors", "actor_name", ["image_url"]),
    "faction": ("factions", "faction_name", ["description", "parody_of", "image_url"]),
    "location": ("locations", "name", ["location_type", "description", "parody_of", "image_url"]),
    "character": ("characters", "character_name",
                  ["full_name", "species", "gender", "character_role", "parody_of", "image_url"]),
    "vehicle": ("vehicles", "vehicle_name", ["vehicle_type", "description", "parody_of", "image_url"]),
    "item": ("items", "item_name", ["item_type", "description", "parody_of", "image_url"]),
    "episode": ("episodes", "title", ["season_number", "episode_number", "air_date", "description"]),
}
# Annotation FK column per entity type.
FK_COLUMN = {"media": "media_id", "actor": "actor_id", "faction": "faction_id",
             "location": "location_id", "character": "character_id", "vehicle": "vehicle_id",
             "item": "item_id", "episode": "episode_id", "quote": "quote_id"}


@dataclass
class Report:
    upserted: dict = field(default_factory=lambda: defaultdict(int))
    created_stubs: list = field(default_factory=list)
    unresolved: list = field(default_factory=list)

    def summary(self):
        lines = [f"  {t}: {n}" for t, n in sorted(self.upserted.items())]
        if self.created_stubs:
            lines.append(f"  actor rows created from cast credits: {len(self.created_stubs)}")
        if self.unresolved:
            lines.append(f"  unresolved names (left null): {len(self.unresolved)}")
            lines += [f"    {u}" for u in self.unresolved]
        return "\n".join(lines)


def _title_from_url(url):
    return urllib.parse.unquote(url.rsplit("/wiki/", 1)[-1]).replace("_", " ")


class Loader:
    def __init__(self, conn):
        self.conn = conn
        self.report = Report()
        self.ids = {t: {} for t in TABLES}           # entity type -> {lowercased name: id}

    # -- pass 1 ------------------------------------------------------------

    def _upsert(self, etype, record, extra=None):
        table, name_col, cols = TABLES[etype]
        values = {name_col: record[name_col], **{c: record.get(c) for c in cols},
                  "source_url": record["source_url"],
                  **(extra or {})}
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT id FROM {table} WHERE source_url = %s", (record["source_url"],))
            row = cur.fetchone()
            if row is None:
                # Adopt a row created earlier from a name only (an actor stub).
                cur.execute(f"SELECT id FROM {table} WHERE lower({name_col}) = lower(%s) "
                            f"AND source_url IS NULL", (values[name_col],))
                row = cur.fetchone()
            assignments = ", ".join(f"{c} = %({c})s" for c in values)
            if row:
                cur.execute(f"UPDATE {table} SET {assignments}, last_updated = now() "
                            f"WHERE id = %(id)s", {**values, "id": row[0]})
                rid = row[0]
            else:
                names = ", ".join(values)
                params = ", ".join(f"%({c})s" for c in values)
                cur.execute(f"INSERT INTO {table} ({names}, last_updated) "
                            f"VALUES ({params}, now()) RETURNING id", values)
                rid = cur.fetchone()[0]
        self._remember(etype, rid, values[name_col], record["source_url"])
        self.report.upserted[table] += 1
        return rid

    def _remember(self, etype, rid, name, source_url=None):
        self.ids[etype].setdefault(name.lower(), rid)
        if source_url:
            self.ids[etype].setdefault(_title_from_url(source_url).lower(), rid)

    def _index_existing(self):
        """Names already in the database count too, so partial loads still link up."""
        with self.conn.cursor() as cur:
            for etype, (table, name_col, _) in TABLES.items():
                cur.execute(f"SELECT id, {name_col}, source_url FROM {table} ORDER BY id")
                for rid, name, url in cur.fetchall():
                    self._remember(etype, rid, name, url)

    # -- pass 2 ------------------------------------------------------------

    def _resolve(self, etype, name, context):
        if not name:
            return None
        rid = self.ids[etype].get(name.lower())
        if rid is None:
            self.report.unresolved.append(f"{context}: no {etype} named {name!r}")
        return rid

    def _actor(self, name):
        rid = self.ids["actor"].get(name.lower())
        if rid is None:
            with self.conn.cursor() as cur:
                cur.execute("INSERT INTO actors (actor_name, last_updated) VALUES (%s, now()) "
                            "RETURNING id", (name,))
                rid = cur.fetchone()[0]
            self._remember("actor", rid, name)
            self.report.created_stubs.append(name)
        return rid

    def _set(self, table, rid, **cols):
        assignments = ", ".join(f"{c} = %({c})s" for c in cols)
        with self.conn.cursor() as cur:
            cur.execute(f"UPDATE {table} SET {assignments} WHERE id = %(id)s", {**cols, "id": rid})

    def _unchanged(self, table, owner_col, owner_id, cols, rows):
        """True when the rows already stored match, so ids don't churn on re-runs."""
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT {', '.join(cols)} FROM {table} WHERE {owner_col} = %s", (owner_id,))
            stored = sorted(cur.fetchall(), key=repr)
        return stored == sorted((tuple(r[c] for c in cols) for r in rows), key=repr)

    def _replace_links(self, table, owner_col, owner_id, rows):
        cols = list(rows[0]) if rows else []
        if rows and self._unchanged(table, owner_col, owner_id, cols, rows):
            return
        with self.conn.cursor() as cur:
            cur.execute(f"DELETE FROM {table} WHERE {owner_col} = %s", (owner_id,))
            for row in rows:
                cols = {owner_col: owner_id, **row}
                cur.execute(f"INSERT INTO {table} ({', '.join(cols)}) "
                            f"VALUES ({', '.join(['%s'] * len(cols))}) ON CONFLICT DO NOTHING",
                            list(cols.values()))

    def _appears_in(self, record, ctx):
        ids = [self._resolve("media", t, ctx) for t in record.get("appears_in", [])]
        return [{"media_id": m} for m in dict.fromkeys(ids) if m]

    def _link(self, etype, rid, record):
        ctx = record["source_url"]
        r = lambda t, n: self._resolve(t, n, ctx)  # noqa: E731
        if etype == "character":
            self._set("characters", rid, faction_id=r("faction", record.get("faction")),
                      homeworld_id=r("location", record.get("homeworld")))
            self._replace_links("media_characters", "character_id", rid, self._appears_in(record, ctx))
            cast = []
            for credit in record.get("portrayed_by", []):
                cast.append({"actor_id": self._actor(credit["actor_name"]),
                             "media_id": r("media", credit.get("media_title")),
                             "credit_type": credit.get("credit_type"), "notes": credit.get("notes")})
            self._replace_links("character_actors", "character_id", rid, cast)
        elif etype == "faction":
            self._set("factions", rid, leader_id=r("character", record.get("leader")))
        elif etype == "location":
            self._set("locations", rid, ruler_id=r("character", record.get("ruler")),
                      heir_id=r("character", record.get("heir")))
            self._replace_links("media_locations", "location_id", rid, self._appears_in(record, ctx))
        elif etype == "vehicle":
            self._set("vehicles", rid, faction_id=r("faction", record.get("faction")))
            self._replace_links("media_vehicles", "vehicle_id", rid, self._appears_in(record, ctx))
            crew = {}
            for member in record.get("crew", []):
                cid = r("character", member["character_name"])
                if cid:
                    crew.setdefault(cid, member.get("crew_role"))
            self._replace_links("vehicle_crew", "vehicle_id", rid,
                                [{"character_id": c, "crew_role": role} for c, role in crew.items()])
        elif etype == "item":
            self._set("items", rid, owner_character_id=r("character", record.get("owner")))

    # -- pass 3 ------------------------------------------------------------

    def _annotations(self, etype, rid, record):
        fk = FK_COLUMN[etype]
        trivia = [{"trivia_kind": t["kind"], "trivia_text": t["text"]} for t in record.get("trivia", [])]
        citations = [{"citation_number": c["number"], "source_text": c["text"], "source_url": c.get("url")}
                     for c in record.get("citations", [])]
        with self.conn.cursor() as cur:
            if etype != "quote" and not self._unchanged("trivia", fk, rid, ["trivia_kind", "trivia_text"], trivia):
                cur.execute(f"DELETE FROM trivia WHERE {fk} = %s", (rid,))
                for t in record.get("trivia", []):
                    cur.execute(f"INSERT INTO trivia (trivia_kind, trivia_text, {fk}) "
                                f"VALUES (%s, %s, %s)", (t["kind"], t["text"], rid))
            if self._unchanged("citations", fk, rid, ["citation_number", "source_text", "source_url"], citations):
                return
            cur.execute(f"DELETE FROM citations WHERE {fk} = %s", (rid,))
            for c in record.get("citations", []):
                cur.execute(f"INSERT INTO citations (citation_number, source_text, source_url, {fk}) "
                            f"VALUES (%s, %s, %s, %s)", (c["number"], c["text"], c.get("url"), rid))

    def _quote(self, record):
        """Quotes are keyed by their text: the same line on two pages is one quote."""
        ctx = record["source_url"]
        values = {"quote_text": record["quote_text"],
                  "character_id": self._resolve("character", record.get("character_name"), ctx),
                  "media_id": self._resolve("media", record.get("media_title"), ctx),
                  "episode_id": self._resolve("episode", record.get("episode_title"), ctx),
                  "source_url": record["source_url"]}
        with self.conn.cursor() as cur:
            cur.execute("SELECT id FROM quotes WHERE quote_text = %s ORDER BY id LIMIT 1",
                        (values["quote_text"],))
            row = cur.fetchone()
            if row:
                cur.execute("UPDATE quotes SET character_id = coalesce(%(character_id)s, character_id), "
                            "media_id = coalesce(%(media_id)s, media_id), "
                            "episode_id = coalesce(%(episode_id)s, episode_id), last_updated = now() "
                            "WHERE id = %(id)s", {**values, "id": row[0]})
                rid = row[0]
            else:
                cur.execute("INSERT INTO quotes (quote_text, character_id, media_id, episode_id, "
                            "source_url, last_updated) VALUES (%(quote_text)s, %(character_id)s, "
                            "%(media_id)s, %(episode_id)s, %(source_url)s, now()) RETURNING id", values)
                rid = cur.fetchone()[0]
        self.report.upserted["quotes"] += 1
        self._annotations("quote", rid, record)

    # -- entry point -------------------------------------------------------

    def load(self, records):
        """records: {entity type: [record, ...]}"""
        self._index_existing()
        ids = {}
        for etype in ["media", "actor", "faction", "location", "character", "vehicle", "item"]:
            for rec in records.get(etype, []):
                ids[(etype, rec["source_url"])] = self._upsert(etype, rec)
        for rec in records.get("episode", []):
            media_id = self._resolve("media", rec["media_title"], rec["source_url"])
            if media_id is not None:
                ids[("episode", rec["source_url"])] = self._upsert("episode", rec, {"media_id": media_id})

        for etype, recs in records.items():
            for rec in recs:
                rid = ids.get((etype, rec.get("source_url")))
                if rid is not None and etype != "quote":
                    self._link(etype, rid, rec)
                    self._annotations(etype, rid, rec)
        for rec in records.get("quote", []):
            self._quote(rec)
        return self.report


def load(dsn, records):
    with psycopg.connect(dsn) as conn:          # commits on success, rolls back on error
        return Loader(conn).load(records)
