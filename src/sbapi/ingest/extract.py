"""
Wikitext -> scrape records (schemas/scrape/). Only what the page states is
copied; anything else stays null or empty, per CLAUDE.md. Nothing here infers
a value from context.
"""

import re
import urllib.parse
from datetime import datetime

import mwparserfromhell

from . import config
from .wiki import page_url

DATE_FORMATS = ["%Y-%m-%d", "%B %d, %Y", "%d %B %Y", "%b %d, %Y", "%d %b %Y"]
DISAMBIGUATOR = re.compile(r"\s*\([^)]*\)$")
SPLIT = re.compile(r"<br\s*/?>|\n", re.IGNORECASE)


def entity_type(categories):
    cats = {c.lower() for c in categories}
    for cat, etype in config.CATEGORY_TYPES:
        if cat.lower() in cats:
            return etype
    return None


def _norm(key):
    return re.sub(r"[\s_\-]+", "", str(key).strip().lower())


def _text(wikicode):
    text = mwparserfromhell.parse(str(wikicode))
    for tag in text.filter_tags(recursive=False):
        if str(tag.tag).lower() == "ref":
            text.remove(tag)
    out = text.strip_code(normalize=True, collapse=True)
    return re.sub(r"\s+", " ", out).strip() or None


def _links(wikicode):
    """Link targets, in order. Falls back to plain text lines when there are none."""
    code = mwparserfromhell.parse(str(wikicode))
    targets = []
    for link in code.filter_wikilinks():
        target = str(link.title).split("#")[0].strip()
        if target and ":" not in target:
            targets.append(target[0].upper() + target[1:])
    if targets:
        return list(dict.fromkeys(targets))
    parts = [_text(p) for p in SPLIT.split(str(code))]
    return [p for p in parts if p]


def _date(value):
    value = _text(value)
    if not value:
        return None
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(value, fmt).date().isoformat()
        except ValueError:
            pass
    return None


def _int(value):
    value = _text(value)
    return int(value) if value and value.isdigit() else None


def _image_url(base_url, value):
    name = _text(value)
    if not name:
        return None
    name = re.sub(r"^(File|Image):", "", name, flags=re.IGNORECASE).strip()
    return f"{base_url.rstrip('/')}/wiki/Special:FilePath/{urllib.parse.quote(name.replace(' ', '_'))}"


def _infobox(code):
    for tpl in code.filter_templates(recursive=False):
        name = _norm(tpl.name)
        if name.startswith("infobox") or name.endswith("infobox"):
            return {_norm(p.name): p.value for p in tpl.params if str(p.value).strip()}
    return {}


def _lead(code):
    """First prose paragraph before any heading, without templates or refs."""
    sections = code.get_sections(include_lead=True, flat=True)
    lead = mwparserfromhell.parse(str(sections[0] if sections else code))
    if lead.filter_headings(recursive=False):
        return None
    for tpl in lead.filter_templates(recursive=False):
        lead.remove(tpl)
    for para in re.split(r"\n\s*\n", str(lead)):
        para = para.strip()
        if para and not para.startswith(("[[File:", "[[Image:", "{|", "__")):
            text = _text(para)
            if text:
                return text
    return None


def _sections(code, wanted):
    """{heading: [bullet text, ...]} for headings in `wanted`."""
    found = {}
    for sec in code.get_sections(flat=True, include_lead=False):
        headings = sec.filter_headings(recursive=False)
        if not headings:
            continue
        title = _text(headings[0].title)
        if not title or title.lower() not in wanted:
            continue
        body = str(sec)[len(str(headings[0])):]
        items = []
        for line in body.splitlines():
            line = line.strip()
            if line.startswith("*"):
                items.append(line.lstrip("*").strip())
        if not items and body.strip():
            items = [p for p in re.split(r"\n\s*\n", body) if p.strip()]
        found[title.lower()] = items
    return found


def _citations(code):
    numbered, seen_names = [], set()
    for tag in code.filter_tags():
        if str(tag.tag).lower() != "ref":
            continue
        name = str(tag.get("name").value).strip() if tag.has("name") else None
        if name and name in seen_names:
            continue
        if not tag.contents or not str(tag.contents).strip():
            continue
        if name:
            seen_names.add(name)
        contents = mwparserfromhell.parse(str(tag.contents))
        urls = [str(l.url) for l in contents.filter_external_links()]
        text = _text(contents)
        if text or urls:
            numbered.append({"number": len(numbered) + 1, "text": text or urls[0],
                             "url": urls[0] if urls else None})
    return numbered


def _quotes(code, source_url):
    quotes = []
    for tpl in code.filter_templates():
        if _norm(tpl.name) not in config.QUOTE_TEMPLATES or not tpl.has(1):
            continue
        text = _text(tpl.get(1).value)
        if not text:
            continue
        speaker = _links(tpl.get(2).value)[0] if tpl.has(2) and _links(tpl.get(2).value) else None
        quotes.append({"quote_text": text, "character_name": speaker, "media_title": None,
                       "episode_title": None, "citations": [], "source_url": source_url})
    return quotes


def extract(page, base_url):
    """Return (record or None, entity type, [quote records], [unmapped infobox keys])."""
    etype = entity_type(page.categories)
    code = mwparserfromhell.parse(page.wikitext)
    source_url = page_url(base_url, page.title)
    quotes = _quotes(code, source_url)
    if etype is None:
        return None, None, quotes, []

    box = _infobox(code)
    mapped, unmapped = {}, []
    for key, value in box.items():
        field = config.FIELD_ALIASES.get(key)
        if field is None:
            unmapped.append(key)
            continue
        mapped.setdefault(field, []).append(value)

    def first_text(field):
        vals = mapped.get(field)
        return _text(vals[0]) if vals else None

    def first_link(field):
        vals = mapped.get(field)
        targets = _links(vals[0]) if vals else []
        return targets[0] if targets else None

    sections = _sections(code, set(config.TRIVIA_SECTIONS) | config.APPEARANCE_SECTIONS)
    trivia = []
    for heading, items in sections.items():
        kind = config.TRIVIA_SECTIONS.get(heading)
        if kind:
            trivia += [{"kind": kind, "text": t} for t in map(_text, items) if t]

    appears_in = []
    for v in mapped.get("appears_in", []):
        appears_in += _links(v)
    for heading in config.APPEARANCE_SECTIONS:
        for item in sections.get(heading, []):
            appears_in += _links(item)[:1]
    appears_in = list(dict.fromkeys(appears_in))

    name = DISAMBIGUATOR.sub("", page.title)
    image_url = _image_url(base_url, mapped["image_url"][0]) if "image_url" in mapped else None
    common = {"source_url": source_url, "trivia": trivia, "citations": _citations(code)}

    if etype == "character":
        portrayed = []
        for field, credit in (("portrayed_by", None), ("portrayed_by:voice", "voice")):
            for v in mapped.get(field, []):
                portrayed += [{"actor_name": a, "media_title": None, "credit_type": credit, "notes": None}
                              for a in _links(v)]
        record = {"character_name": name, "full_name": first_text("full_name"),
                  "species": first_text("species"), "gender": first_text("gender"),
                  "character_role": first_text("character_role"), "parody_of": first_text("parody_of"),
                  "faction": first_link("faction"), "homeworld": first_link("homeworld"),
                  "image_url": image_url, "appears_in": appears_in, "portrayed_by": portrayed, **common}
    elif etype == "media":
        record = {"title": name, "media_type": None, "release_date": _date(mapped["release_date"][0])
                  if "release_date" in mapped else None, "description": _lead(code),
                  "image_url": image_url, **common}
    elif etype == "episode":
        media_title = first_link("media_title")
        if media_title is None:
            return None, etype, quotes, unmapped
        record = {"title": name, "media_title": media_title,
                  "season_number": _int(mapped["season_number"][0]) if "season_number" in mapped else None,
                  "episode_number": _int(mapped["episode_number"][0]) if "episode_number" in mapped else None,
                  "air_date": _date(mapped["air_date"][0]) if "air_date" in mapped else None,
                  "description": _lead(code), **common}
    elif etype == "actor":
        record = {"actor_name": name, "image_url": image_url, **common}
    elif etype == "faction":
        record = {"faction_name": name, "description": _lead(code), "leader": first_link("leader"),
                  "parody_of": first_text("parody_of"), "image_url": image_url, **common}
    elif etype == "location":
        record = {"name": name, "location_type": first_text("type"), "description": _lead(code),
                  "ruler": first_link("ruler"), "heir": first_link("heir"),
                  "parody_of": first_text("parody_of"), "image_url": image_url,
                  "appears_in": appears_in, **common}
    elif etype == "vehicle":
        crew = []
        for field, vals in mapped.items():
            if field == "crew" or field.startswith("crew:"):
                role = field.split(":", 1)[1] if ":" in field else None
                for v in vals:
                    crew += [{"character_name": c, "crew_role": role} for c in _links(v)]
        record = {"vehicle_name": name, "vehicle_type": first_text("type"), "description": _lead(code),
                  "faction": first_link("faction"), "parody_of": first_text("parody_of"),
                  "image_url": image_url, "appears_in": appears_in, "crew": crew, **common}
    elif etype == "item":
        item_type = next((config.ITEM_TYPE_BY_CATEGORY[c] for c in page.categories
                          if c in config.ITEM_TYPE_BY_CATEGORY), "other")
        record = {"item_name": name, "item_type": item_type, "description": _lead(code),
                  "owner": first_link("owner"), "parody_of": first_text("parody_of"),
                  "image_url": image_url, **common}
    else:
        return None, etype, quotes, unmapped
    return record, etype, quotes, unmapped
