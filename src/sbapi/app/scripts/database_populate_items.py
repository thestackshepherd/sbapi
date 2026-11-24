"""
Data for the items table (weapons, artifacts, tech, and merchandise).

Populating logic lives in database_populate_main.py. Owners are referenced by
character_name ("owner_character_name") and resolved to an id at insert time.
"""

from datetime import UTC, datetime

NOW = datetime.now(UTC)

WIKI = "https://spaceballs.fandom.com/wiki/"
MERCH = WIKI + "Spaceballs:_The..."

THE_SCHWARTZ_DESCRIPTION = """
    Supernatural force with an upside (good) and a downside (bad). Lets users
    move objects, create energy blades, and shoot energy bolts. Yogurt is its
    keeper.
"""
RING_OF_THE_SCHWARTZ_DESCRIPTION = """
    Yogurt's upside Schwartz-ring, with a capital S written in 12 gems; makes
    a yellow blade. Given to Lone Starr. Yogurt admits it came from a Cracker
    Jack box.
"""
DOWNSIDE_RING_DESCRIPTION = """
    Dark Helmet's downside Schwartz-ring, shaped like a snake with a jewel in
    its mouth; makes a green blade.
"""
LIQUID_SCHWARTZ_DESCRIPTION = """
    Canned fuel from Yogurt. Barf pours it into the Eagle 5's tank to speed
    back to Druidia for Vespa's wedding.
"""
SELF_DESTRUCT_BUTTON_DESCRIPTION = """
    Button on Spaceball One / Mega Maid that destroys the whole ship. Dark
    Helmet presses it by accident; the cancellation button is out of order.
"""
PERRI_AIR_DESCRIPTION = """
    Canned, naturally sparkling, salt-free air, 'Canned in Druidia'. One of
    the few sources of air in Spaceball City; Skroob keeps cans in his desk.
"""
AIR_SHIELD_DESCRIPTION = """
    Shield around Planet Druidia that holds in its air. Combination: 1-2-3-4-5.
"""
MR_COFFEE_DESCRIPTION = """
    Overly complex coffee machine on Spaceball One, right next to Mr. Radar.
"""
MR_RADAR_DESCRIPTION = """
    Device on Spaceball One that tracks nearby ships and planets.
"""
MR_RENTAL_DESCRIPTION = """
    Video cassette rental device on Spaceball One, stocked with Mel Brooks
    films; used to find the instant cassette of Spaceballs.
"""
VIRGIN_ALARM_DESCRIPTION = """
    Alarm a Droid of Honor is fitted with to keep an engaged princess chaste.
    Goes off before Vespa and Lone Starr can kiss.
"""
JAM_DESCRIPTION = """
    Raspberry jam fired from the Eagle 5 to jam Spaceball One's radar.
"""
SPACEBUCKS_DESCRIPTION = """
    Common currency. Lone Starr owes Pizza the Hutt 1,000,000 spacebucks.
"""
XG_95_DESCRIPTION = """
    Magnetic beam the Spaceballs use to pull Vespa's car aboard Spaceball One.
"""

ITEMS = [
    # --- The Schwartz ---
    {
        "item_name": "The Schwartz",
        "item_type": "other",  # a force, not an object
        "description": THE_SCHWARTZ_DESCRIPTION,
        "parody_of": "The Force (Star Wars)",
        "owner_character_name": None,
        "image_url": None,
        "source_url": WIKI + "The_Schwartz",
        "last_updated": NOW,
    },
    {
        "item_name": "Ring of the Schwartz",  # name from Spaceballs: The Book
        "item_type": "weapon",
        "description": RING_OF_THE_SCHWARTZ_DESCRIPTION,
        "parody_of": "Lightsaber (Star Wars)",
        "owner_character_name": "Lone Starr",  # Yogurt's, lets Lone Starr keep it
        "image_url": None,
        "source_url": WIKI + "Schwartz-ring",
        "last_updated": NOW,
    },
    {
        "item_name": "Downside Schwartz-ring",
        "item_type": "weapon",
        "description": DOWNSIDE_RING_DESCRIPTION,
        "parody_of": "Lightsaber (Star Wars)",
        "owner_character_name": "Dark Helmet",
        "image_url": None,
        "source_url": WIKI + "Schwartz-ring",
        "last_updated": NOW,
    },
    {
        "item_name": "Liquid Schwartz",
        "item_type": "other",
        "description": LIQUID_SCHWARTZ_DESCRIPTION,
        "parody_of": None,
        "owner_character_name": None,
        "image_url": None,
        "source_url": WIKI + "Liquid_Schwartz",
        "last_updated": NOW,
    },
    # --- Spaceball One ---
    {
        "item_name": "Self-destruct button",
        "item_type": "tech",
        "description": SELF_DESTRUCT_BUTTON_DESCRIPTION,
        "parody_of": None,
        "owner_character_name": None,
        "image_url": None,
        "source_url": WIKI + "Self-destruct_button",
        "last_updated": NOW,
    },
    {
        "item_name": "Mr. Coffee",
        "item_type": "tech",
        "description": MR_COFFEE_DESCRIPTION,
        "parody_of": None,
        "owner_character_name": None,
        "image_url": None,
        "source_url": WIKI + "Mr._Coffee",
        "last_updated": NOW,
    },
    {
        "item_name": "Mr. Radar",
        "item_type": "tech",
        "description": MR_RADAR_DESCRIPTION,
        "parody_of": None,
        "owner_character_name": None,
        "image_url": None,
        "source_url": WIKI + "Mr._Radar",
        "last_updated": NOW,
    },
    {
        "item_name": "Mr. Rental",
        "item_type": "tech",
        "description": MR_RENTAL_DESCRIPTION,
        "parody_of": None,
        "owner_character_name": None,
        "image_url": None,
        "source_url": WIKI + "Mr._Rental",
        "last_updated": NOW,
    },
    {
        "item_name": "XG-95",  # only described in Spaceballs: The Book
        "item_type": "tech",
        "description": XG_95_DESCRIPTION,
        "parody_of": None,
        "owner_character_name": None,
        "image_url": None,
        "source_url": WIKI + "XG-95",
        "last_updated": NOW,
    },
    # --- Druidia ---
    {
        "item_name": "Air shield",
        "item_type": "tech",
        "description": AIR_SHIELD_DESCRIPTION,
        "parody_of": None,
        "owner_character_name": None,
        "image_url": None,
        "source_url": WIKI + "Air_shield",
        "last_updated": NOW,
    },
    {
        "item_name": "Perri-Air",
        "item_type": "other",
        "description": PERRI_AIR_DESCRIPTION,
        "parody_of": None,
        "owner_character_name": None,
        "image_url": None,
        "source_url": WIKI + "Perri-Air",
        "last_updated": NOW,
    },
    {
        "item_name": "Virgin Alarm",
        "item_type": "tech",
        "description": VIRGIN_ALARM_DESCRIPTION,
        "parody_of": None,
        "owner_character_name": "Dot Matrix",
        "image_url": None,
        "source_url": WIKI + "Virgin_Alarm",
        "last_updated": NOW,
    },
    # --- Eagle 5 ---
    {
        "item_name": "Jam",
        "item_type": "other",
        "description": JAM_DESCRIPTION,
        "parody_of": None,
        "owner_character_name": None,
        "image_url": None,
        "source_url": WIKI + "Jam",
        "last_updated": NOW,
    },
    # --- Misc ---
    {
        "item_name": "Spacebucks",
        "item_type": "other",
        "description": SPACEBUCKS_DESCRIPTION,
        "parody_of": None,
        "owner_character_name": None,
        "image_url": None,
        "source_url": WIKI + "Spacebucks",
        "last_updated": NOW,
    },
    # --- Merchandise (Yogurt shows these to the heroes) ---
    {
        "item_name": "Spaceballs: The T-Shirt",
        "item_type": "merchandise",
        "description": None,
        "parody_of": None,
        "owner_character_name": "Yogurt",
        "image_url": None,
        "source_url": MERCH,
        "last_updated": NOW,
    },
    {
        "item_name": "Spaceballs: The Coloring Book",
        "item_type": "merchandise",
        "description": None,
        "parody_of": None,
        "owner_character_name": "Yogurt",
        "image_url": None,
        "source_url": MERCH,
        "last_updated": NOW,
    },
    {
        "item_name": "Spaceballs: The Lunchbox",
        "item_type": "merchandise",
        "description": None,
        "parody_of": None,
        "owner_character_name": "Yogurt",
        "image_url": None,
        "source_url": MERCH,
        "last_updated": NOW,
    },
    {
        "item_name": "Spaceballs: The Breakfast Cereal",
        "item_type": "merchandise",
        "description": None,
        "parody_of": None,
        "owner_character_name": "Yogurt",
        "image_url": None,
        "source_url": MERCH,
        "last_updated": NOW,
    },
    {
        "item_name": "Spaceballs: The Flamethrower",
        "item_type": "merchandise",
        "description": "Sold as 'A Children's Toy'. \"The kids love this one!\"",
        "parody_of": None,
        "owner_character_name": "Yogurt",
        "image_url": None,
        "source_url": MERCH,
        "last_updated": NOW,
    },
    {
        "item_name": "Spaceballs: The Doll",
        "item_type": "merchandise",
        "description": "A Yogurt doll.",
        "parody_of": None,
        "owner_character_name": "Yogurt",
        "image_url": None,
        "source_url": MERCH,
        "last_updated": NOW,
    },
]
