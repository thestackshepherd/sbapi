"""
Data for the items table (weapons, artifacts, tech, and merchandise).

Populating logic lives in database_populate_main.py. Owners are referenced by
character_name ("owner_character_name") and resolved to an id at insert time.
"""
from datetime import UTC, datetime

NOW = datetime.now(UTC)

WIKI = "https://spaceballs.fandom.com/wiki/"
MERCH = WIKI + "Spaceballs:_The..."

the_schwartz_description = (
    "Supernatural force with an upside (good) and a downside (bad). Lets users "
    "move objects, create energy blades, and shoot energy bolts. Yogurt is its "
    "keeper."
)
ring_of_the_schwartz_description = (
    "Yogurt's upside Schwartz-ring, with a capital S written in 12 gems; makes "
    "a yellow blade. Given to Lone Starr. Yogurt admits it came from a Cracker "
    "Jack box."
)
downside_ring_description = (
    "Dark Helmet's downside Schwartz-ring, shaped like a snake with a jewel in "
    "its mouth; makes a green blade."
)
liquid_schwartz_description = (
    "Canned fuel from Yogurt. Barf pours it into the Eagle 5's tank to speed "
    "back to Druidia for Vespa's wedding."
)
self_destruct_button_description = (
    "Button on Spaceball One / Mega Maid that destroys the whole ship. Dark "
    "Helmet presses it by accident; the cancellation button is out of order."
)
perri_air_description = (
    "Canned, naturally sparkling, salt-free air, 'Canned in Druidia'. One of "
    "the few sources of air in Spaceball City; Skroob keeps cans in his desk."
)
air_shield_description = (
    "Shield around Planet Druidia that holds in its air. Combination: 1-2-3-4-5."
)
mr_coffee_description = (
    "Overly complex coffee machine on Spaceball One, right next to Mr. Radar."
)
mr_radar_description = (
    "Device on Spaceball One that tracks nearby ships and planets."
)
mr_rental_description = (
    "Video cassette rental device on Spaceball One, stocked with Mel Brooks "
    "films; used to find the instant cassette of Spaceballs."
)
virgin_alarm_description = (
    "Alarm a Droid of Honor is fitted with to keep an engaged princess chaste. "
    "Goes off before Vespa and Lone Starr can kiss."
)
jam_description = (
    "Raspberry jam fired from the Eagle 5 to jam Spaceball One's radar."
)
spacebucks_description = (
    "Common currency. Lone Starr owes Pizza the Hutt 1,000,000 spacebucks."
)
xg_95_description = (
    "Magnetic beam the Spaceballs use to pull Vespa's car aboard Spaceball One."
)

ITEMS = [
    # --- The Schwartz ---
    {
        "item_name": "The Schwartz",
        "item_type": "other",  # a force, not an object
        "description": the_schwartz_description,
        "parody_of": "The Force (Star Wars)",
        "owner_character_name": None,
        "image_url": None,
        "source_url": WIKI + "The_Schwartz",
        "last_updated": NOW,
    },
    {
        "item_name": "Ring of the Schwartz",  # name from Spaceballs: The Book
        "item_type": "weapon",
        "description": ring_of_the_schwartz_description,
        "parody_of": "Lightsaber (Star Wars)",
        "owner_character_name": "Lone Starr",  # Yogurt's, lets Lone Starr keep it
        "image_url": None,
        "source_url": WIKI + "Schwartz-ring",
        "last_updated": NOW,
    },
    {
        "item_name": "Downside Schwartz-ring",
        "item_type": "weapon",
        "description": downside_ring_description,
        "parody_of": "Lightsaber (Star Wars)",
        "owner_character_name": "Dark Helmet",
        "image_url": None,
        "source_url": WIKI + "Schwartz-ring",
        "last_updated": NOW,
    },
    {
        "item_name": "Liquid Schwartz",
        "item_type": "other",
        "description": liquid_schwartz_description,
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
        "description": self_destruct_button_description,
        "parody_of": None,
        "owner_character_name": None,
        "image_url": None,
        "source_url": WIKI + "Self-destruct_button",
        "last_updated": NOW,
    },
    {
        "item_name": "Mr. Coffee",
        "item_type": "tech",
        "description": mr_coffee_description,
        "parody_of": None,
        "owner_character_name": None,
        "image_url": None,
        "source_url": WIKI + "Mr._Coffee",
        "last_updated": NOW,
    },
    {
        "item_name": "Mr. Radar",
        "item_type": "tech",
        "description": mr_radar_description,
        "parody_of": None,
        "owner_character_name": None,
        "image_url": None,
        "source_url": WIKI + "Mr._Radar",
        "last_updated": NOW,
    },
    {
        "item_name": "Mr. Rental",
        "item_type": "tech",
        "description": mr_rental_description,
        "parody_of": None,
        "owner_character_name": None,
        "image_url": None,
        "source_url": WIKI + "Mr._Rental",
        "last_updated": NOW,
    },
    {
        "item_name": "XG-95",  # only described in Spaceballs: The Book
        "item_type": "tech",
        "description": xg_95_description,
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
        "description": air_shield_description,
        "parody_of": None,
        "owner_character_name": None,
        "image_url": None,
        "source_url": WIKI + "Air_shield",
        "last_updated": NOW,
    },
    {
        "item_name": "Perri-Air",
        "item_type": "other",
        "description": perri_air_description,
        "parody_of": None,
        "owner_character_name": None,
        "image_url": None,
        "source_url": WIKI + "Perri-Air",
        "last_updated": NOW,
    },
    {
        "item_name": "Virgin Alarm",
        "item_type": "tech",
        "description": virgin_alarm_description,
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
        "description": jam_description,
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
        "description": spacebucks_description,
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
