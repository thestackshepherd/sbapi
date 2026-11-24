"""
Data for the citations table (numbered sources backing an entity's data).

Populating logic lives in database_populate_main.py. Each row names exactly one
entity by its natural key (vehicle_name or item_name here), resolved to an id at
insert time. Each entity's sources are numbered from 1, in the order its wiki
page's References list gives them.
"""

WIKI = "https://spaceballs.fandom.com/wiki/"

FILM = "Spaceballs (1987 film)"
BOOK = "Spaceballs: The Book (novelization)"

CITATIONS = [
    # --- Vehicles ---
    {
        "vehicle_name": "Spaceball One",
        "citation_number": 1,
        "source_text": BOOK,
        "source_url": WIKI + "Spaceball_I",
    },
    {
        "vehicle_name": "Spaceball One",
        "citation_number": 2,
        "source_text": FILM,
        "source_url": WIKI + "Spaceball_I",
    },
    {
        "vehicle_name": "Mega Maid",
        "citation_number": 1,
        "source_text": FILM,
        "source_url": WIKI + "Mega_Maid",
    },
    {
        "vehicle_name": "Honeymoon Cruise",
        "citation_number": 1,
        "source_text": BOOK,
        "source_url": WIKI + "Honeymoon_Cruise",
    },
    {
        "vehicle_name": "Honeymoon Cruise",
        "citation_number": 2,
        "source_text": FILM,
        "source_url": WIKI + "Honeymoon_Cruise",
    },
    # --- Items ---
    {
        "item_name": "The Schwartz",
        "citation_number": 1,
        "source_text": FILM,
        "source_url": WIKI + "The_Schwartz",
    },
    {
        "item_name": "Ring of the Schwartz",
        "citation_number": 1,
        "source_text": BOOK,
        "source_url": WIKI + "Schwartz-ring",
    },
    {
        "item_name": "Ring of the Schwartz",
        "citation_number": 2,
        "source_text": FILM,
        "source_url": WIKI + "Schwartz-ring",
    },
    {
        "item_name": "Downside Schwartz-ring",
        "citation_number": 1,
        "source_text": FILM,
        "source_url": WIKI + "Schwartz-ring",
    },
    {
        "item_name": "Liquid Schwartz",
        "citation_number": 1,
        "source_text": FILM,
        "source_url": WIKI + "Liquid_Schwartz",
    },
    {
        "item_name": "Self-destruct button",
        "citation_number": 1,
        "source_text": FILM,
        "source_url": WIKI + "Self-destruct_button",
    },
    {
        "item_name": "Mr. Coffee",
        "citation_number": 1,
        "source_text": FILM,
        "source_url": WIKI + "Mr._Coffee",
    },
    {
        "item_name": "Mr. Radar",
        "citation_number": 1,
        "source_text": FILM,
        "source_url": WIKI + "Mr._Radar",
    },
    {
        "item_name": "Mr. Rental",
        "citation_number": 1,
        "source_text": FILM,
        "source_url": WIKI + "Mr._Rental",
    },
    {
        "item_name": "XG-95",
        "citation_number": 1,
        "source_text": BOOK,
        "source_url": WIKI + "XG-95",
    },
    {
        "item_name": "Air shield",
        "citation_number": 1,
        "source_text": FILM,
        "source_url": WIKI + "Air_shield",
    },
    {
        "item_name": "Perri-Air",
        "citation_number": 1,
        "source_text": FILM,
        "source_url": WIKI + "Perri-Air",
    },
    {
        "item_name": "Virgin Alarm",
        "citation_number": 1,
        "source_text": FILM,
        "source_url": WIKI + "Virgin_Alarm",
    },
    {
        "item_name": "Jam",
        "citation_number": 1,
        "source_text": FILM,
        "source_url": WIKI + "Jam",
    },
    {
        "item_name": "Jam",
        "citation_number": 2,
        "source_text": BOOK,
        "source_url": WIKI + "Jam",
    },
    {
        "item_name": "Spacebucks",
        "citation_number": 1,
        "source_text": FILM,
        "source_url": WIKI + "Spacebucks",
    },
]
