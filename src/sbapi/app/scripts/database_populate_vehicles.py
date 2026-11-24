"""
Data for the vehicles table (ships and other vehicles).

Populating logic lives in database_populate_main.py.
"""
from datetime import UTC, datetime

NOW = datetime.now(UTC)

WIKI = "https://spaceballs.fandom.com/wiki/"

eagle_5_description = (
    "Lone Starr and Barf's flying Winnebago, used to rescue Princess Vespa "
    "and to blow up Spaceball One. Has a periscope, secret hyperjets, and an "
    "infrared scanner."
)
spaceball_one_description = (
    "Extremely long Spaceball star cruiser commanded by Dark Helmet. Holds a "
    "shopping mall, a three-ring circus, and a zoo, and can transform into "
    "Mega Maid."
)
mega_maid_description = (
    "Transformed version of Spaceball One, shaped like a woman with a vacuum "
    "cleaner, used to suck the air off Planet Druidia. Self-destructs; its "
    "head crash-lands on the Planet of the Apes."
)
honeymoon_cruise_description = (
    "Princess Vespa's 2001 Mercedes-Benz SEL Limited Edition space car, used "
    "to run away from her wedding to Prince Valium. Pulled aboard Spaceball "
    "One after Lone Starr rescues Vespa."
)
bladder_ship_description = (
    "Large bladder-shaped Spaceball cruiser that drops smaller ball-shaped "
    "ships from its bottom as deployment pods for soldiers."
)

VEHICLES = [
    # --- Heroes ---
    {
        "vehicle_name": "Eagle 5",
        "vehicle_type": "Winnebago",  # a 1986 Winnebago Chieftain 33
        "description": eagle_5_description,
        "parody_of": "Millennium Falcon (Star Wars)",
        "image_url": None,
        "source_url": WIKI + "Eagle_5",
        "last_updated": NOW,
    },
    {
        "vehicle_name": "Honeymoon Cruise",  # name from Spaceballs: The Book
        "vehicle_type": "Space car",
        "description": honeymoon_cruise_description,
        "parody_of": None,
        "image_url": None,
        "source_url": WIKI + "Honeymoon_Cruise",
        "last_updated": NOW,
    },

    # --- Spaceballs ---
    {
        "vehicle_name": "Spaceball One",  # wiki title is "Spaceball I"
        "vehicle_type": "Spaceball Star Cruiser",
        "description": spaceball_one_description,
        "parody_of": "Executor / Star Destroyer and the Death Star (Star Wars)",
        "image_url": None,
        "source_url": WIKI + "Spaceball_I",
        "last_updated": NOW,
    },
    {
        "vehicle_name": "Mega Maid",
        "vehicle_type": "Transformed star cruiser",
        "description": mega_maid_description,
        "parody_of": None,  # wiki only speculates (Unicron, Statue of Liberty)
        "image_url": None,
        "source_url": WIKI + "Mega_Maid",
        "last_updated": NOW,
    },

    # --- Sequel: Spaceballs: The New One (2027) ---
    {
        "vehicle_name": "Bladder Ship",
        "vehicle_type": "Cruiser",
        "description": bladder_ship_description,
        "parody_of": None,
        "image_url": None,
        "source_url": WIKI + "Bladder_Ship",
        "last_updated": NOW,
    },
]
