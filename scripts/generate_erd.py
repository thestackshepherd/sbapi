#!/usr/bin/env python3
"""Generate a Mermaid ER diagram + table reference from the SQL schema file.

Usage:
    uv run python scripts/generate_erd.py
    uv run python scripts/generate_erd.py --schema path/to/schema.sql --output docs/ERD.md
"""

import argparse
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SCHEMA = REPO_ROOT / "src/sbapi/app/database/sbapidatabase_schema.sql"
DEFAULT_OUTPUT = REPO_ROOT / "docs/ERD.md"

CREATE_TABLE_RE = re.compile(
    r"CREATE TABLE IF NOT EXISTS\s+(\w+)\s*\((.*?)\n\);",
    re.DOTALL | re.IGNORECASE,
)
ALTER_COLUMN_RE = re.compile(
    r"ALTER TABLE\s+(\w+)\s+ADD COLUMN IF NOT EXISTS\s+(\w+)\s+(.*?);",
    re.IGNORECASE,
)
REFERENCES_RE = re.compile(r"REFERENCES\s+(\w+)\s*\(", re.IGNORECASE)

TABLE_LEVEL_CONSTRAINT_PREFIXES = ("UNIQUE", "CHECK", "PRIMARY KEY", "FOREIGN KEY")

SQL_TO_MERMAID_TYPE = {
    "SERIAL": "int",
    "INTEGER": "int",
    "VARCHAR": "string",
    "TEXT": "string",
    "TIMESTAMPTZ": "timestamp",
    "DATE": "date",
}


class Table:
    def __init__(self, name: str):
        self.name = name
        self.columns: list[dict] = []

    def add_column(self, name: str, type_: str, pk: bool, fk_table: str | None, notnull: bool):
        self.columns.append(
            {"name": name, "type": type_, "pk": pk, "fk_table": fk_table, "notnull": notnull}
        )


def split_top_level(body: str) -> list[str]:
    """Split a CREATE TABLE body into comma-separated definitions, ignoring
    commas nested inside parentheses (e.g. a CHECK (... IN (a, b, c)) clause)."""
    parts, depth, current = [], 0, []
    for ch in body:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(ch)
    tail = "".join(current).strip()
    if tail:
        parts.append(tail)
    return parts


def sql_type_to_mermaid(sql_type: str) -> str:
    return SQL_TO_MERMAID_TYPE.get(sql_type.upper(), sql_type.lower() or "unknown")


def parse_column_def(item: str) -> dict | None:
    upper_item = item.upper()
    if upper_item.startswith(TABLE_LEVEL_CONSTRAINT_PREFIXES):
        return None
    tokens = item.split()
    if not tokens:
        return None
    name, type_ = tokens[0], tokens[1] if len(tokens) > 1 else ""
    fk_match = REFERENCES_RE.search(item)
    return {
        "name": name,
        "type_": type_,
        "pk": "PRIMARY KEY" in upper_item,
        "fk_table": fk_match.group(1) if fk_match else None,
        "notnull": "NOT NULL" in upper_item,
    }


def parse_schema(sql: str) -> dict[str, Table]:
    tables: dict[str, Table] = {}

    for match in CREATE_TABLE_RE.finditer(sql):
        table_name, body = match.group(1), match.group(2)
        # A later CREATE TABLE for a name already seen (e.g. after a DROP TABLE)
        # replaces that table's definition rather than merging into it.
        table = Table(table_name)
        tables[table_name] = table
        for item in split_top_level(body):
            col = parse_column_def(item)
            if col:
                table.add_column(**col)

    for match in ALTER_COLUMN_RE.finditer(sql):
        table_name, col_name, rest = match.groups()
        table = tables.setdefault(table_name, Table(table_name))
        fk_match = REFERENCES_RE.search(rest)
        type_ = rest.split()[0] if rest.split() else ""
        table.add_column(
            col_name,
            type_,
            pk=False,
            fk_table=fk_match.group(1) if fk_match else None,
            notnull="NOT NULL" in rest.upper(),
        )

    return tables


def build_relationships(tables: dict[str, Table]) -> list[tuple[str, str, str, bool]]:
    """Return (parent_table, child_table, fk_column, not_null) for every FK found."""
    relationships = []
    for table in tables.values():
        for col in table.columns:
            if col["fk_table"]:
                relationships.append((col["fk_table"], table.name, col["name"], col["notnull"]))
    return relationships


def render_mermaid(tables: dict[str, Table], relationships: list[tuple[str, str, str, bool]]) -> str:
    lines = ["erDiagram"]
    for table in sorted(tables.values(), key=lambda t: t.name):
        lines.append(f"    {table.name} {{")
        for col in table.columns:
            keys = [k for k, present in (("PK", col["pk"]), ("FK", bool(col["fk_table"]))) if present]
            key_str = f" {','.join(keys)}" if keys else ""
            lines.append(f"        {sql_type_to_mermaid(col['type'])} {col['name']}{key_str}")
        lines.append("    }")
    for parent, child, column, notnull in relationships:
        many_side = "|{" if notnull else "o{"
        lines.append(f'    {parent} ||--{many_side} {child} : "{column}"')
    return "\n".join(lines)


def render_markdown(tables: dict[str, Table], relationships: list[tuple[str, str, str, bool]]) -> str:
    out = [
        "# SBAPI Entity Relationship Diagram",
        "",
        "Auto-generated from `sbapidatabase_schema.sql` by `scripts/generate_erd.py`. "
        "Do not edit by hand — rerun the script after changing the schema.",
        "",
        "```mermaid",
        render_mermaid(tables, relationships),
        "```",
        "",
        "## Tables",
        "",
    ]
    for table in sorted(tables.values(), key=lambda t: t.name):
        out.append(f"### {table.name}")
        out.append("")
        out.append("| Column | Type | Key |")
        out.append("|---|---|---|")
        for col in table.columns:
            keys = []
            if col["pk"]:
                keys.append("PK")
            if col["fk_table"]:
                keys.append(f"FK → {col['fk_table']}")
            out.append(f"| {col['name']} | {col['type']} | {', '.join(keys)} |")
        out.append("")
    return "\n".join(out)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA, help="Path to the SQL schema file")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Path to write the ERD markdown file")
    args = parser.parse_args()

    sql = args.schema.read_text()
    tables = parse_schema(sql)
    relationships = build_relationships(tables)
    markdown = render_markdown(tables, relationships)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(markdown)
    print(f"Wrote ERD for {len(tables)} tables ({len(relationships)} relationships) to {args.output}")


if __name__ == "__main__":
    main()
