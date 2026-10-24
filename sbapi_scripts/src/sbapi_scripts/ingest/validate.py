"""
Check scrape records against schemas/scrape/*.schema.json (draft 2020-12).
"""

import json
from functools import cache
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

SCHEMA_DIR = Path(__file__).resolve().parents[4] / "schemas" / "scrape"
ENTITY_TYPES = ["media", "episode", "actor", "faction", "location", "character",
                "vehicle", "item", "quote"]


@cache
def _registry(schema_dir=SCHEMA_DIR):
    resources = []
    for path in schema_dir.glob("*.schema.json"):
        schema = json.loads(path.read_text())
        resource = Resource.from_contents(schema)
        resources += [(schema["$id"], resource), (path.name, resource)]
    return Registry().with_resources(resources)


@cache
def validator(entity_type, schema_dir=SCHEMA_DIR):
    schema = json.loads((schema_dir / f"{entity_type}.schema.json").read_text())
    return Draft202012Validator(schema, registry=_registry(schema_dir),
                                format_checker=FormatChecker())


def errors(entity_type, record):
    """List of human-readable problems; empty when the record is valid."""
    return [f"{'/'.join(map(str, e.absolute_path)) or '<root>'}: {e.message}"
            for e in validator(entity_type).iter_errors(record)]
