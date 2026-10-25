# Scrape schemas

JSON Schemas (draft 2020-12) for the records a scraper fills in from the
Spaceballs wiki, one file per entity. `common.schema.json` holds the shared
pieces (trivia, citations, source URL).

- One JSON object per wiki page, validated against the entity's schema.
- Links to other records are by **name** (e.g. `"faction": "Spaceballs"`), not by
  database id. The loader resolves names to ids when inserting.
- Anything the page doesn't state is `null` or an empty array. Never guess a
  value (see `CLAUDE.md`).

Each schema maps onto `sbapi_scripts/src/sbapi_scripts/db/schema.sql`:
nested `trivia`/`citations` go to the shared `trivia`/`citations` tables,
`appears_in` to `media_*`, `portrayed_by` to `character_actors`, and
`crew` to `vehicle_crew`.
