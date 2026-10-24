"""
How wiki pages map onto scrape records. This is the part to tune after the
first real run: `python -m sbapi_scripts.ingest report` lists the categories and
infobox fields the wiki actually uses, and which ones nothing here maps.
"""

# Wiki category -> entity type. A page takes the first type whose category it has,
# in this order, so a more specific category should come first.
CATEGORY_TYPES = [
    ("Episodes", "episode"),
    ("Films", "media"),
    ("Media", "media"),
    ("Television series", "media"),
    ("Cast", "actor"),
    ("Actors", "actor"),
    ("Real-world people", "actor"),
    ("Factions", "faction"),
    ("Organizations", "faction"),
    ("Groups", "faction"),
    ("Vehicles", "vehicle"),
    ("Spaceships", "vehicle"),
    ("Starships", "vehicle"),
    ("Ships", "vehicle"),
    ("Planets", "location"),
    ("Locations", "location"),
    ("Places", "location"),
    ("Weapons", "item"),
    ("Items", "item"),
    ("Objects", "item"),
    ("Technology", "item"),
    ("Merchandise", "item"),
    ("Characters", "character"),
]

# item_type is required by the schema, so it comes only from a category that says it.
ITEM_TYPE_BY_CATEGORY = {
    "Weapons": "weapon",
    "Technology": "tech",
    "Merchandise": "merchandise",
}

# Infobox parameter (lowercased, spaces/underscores folded) -> record field.
# Fields in LINK_FIELDS take wiki link targets, so names match page titles.
FIELD_ALIASES = {
    "fullname": "full_name",
    "realname": "full_name",
    "species": "species",
    "race": "species",
    "gender": "gender",
    "sex": "gender",
    "occupation": "character_role",
    "role": "character_role",
    "title": "character_role",
    "position": "character_role",
    "parody": "parody_of",
    "parodyof": "parody_of",
    "parodies": "parody_of",
    "basedon": "parody_of",
    "affiliation": "faction",
    "faction": "faction",
    "allegiance": "faction",
    "homeworld": "homeworld",
    "homeplanet": "homeworld",
    "home": "homeworld",
    "origin": "homeworld",
    "image": "image_url",
    "appearances": "appears_in",
    "appearsin": "appears_in",
    "appearance": "appears_in",
    "portrayedby": "portrayed_by",
    "actor": "portrayed_by",
    "actress": "portrayed_by",
    "playedby": "portrayed_by",
    "voice": "portrayed_by:voice",
    "voicedby": "portrayed_by:voice",
    "voiceactor": "portrayed_by:voice",
    "type": "type",
    "class": "type",
    "leader": "leader",
    "leaders": "leader",
    "ruler": "ruler",
    "rulers": "ruler",
    "heir": "heir",
    "owner": "owner",
    "owners": "owner",
    "pilot": "crew:pilot",
    "pilots": "crew:pilot",
    "captain": "crew:captain",
    "copilot": "crew:co-pilot",
    "crew": "crew",
    "releasedate": "release_date",
    "release": "release_date",
    "released": "release_date",
    "airdate": "air_date",
    "season": "season_number",
    "episode": "episode_number",
    "episodenumber": "episode_number",
    "series": "media_title",
}

LINK_FIELDS = {"faction", "homeworld", "appears_in", "portrayed_by", "leader",
               "ruler", "heir", "owner", "crew", "media_title"}

# Section heading (lowercased) -> trivia kind.
TRIVIA_SECTIONS = {
    "trivia": "trivia",
    "notes": "trivia",
    "behind the scenes": "behind_the_scenes",
    "production notes": "behind_the_scenes",
}

APPEARANCE_SECTIONS = {"appearances", "appearance"}

# Templates holding a line of dialogue: first positional param is the line,
# second is the speaker.
QUOTE_TEMPLATES = {"quote", "quotation", "dialogue"}
