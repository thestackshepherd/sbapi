"""
Data for the vehicle_crew table (who is aboard a vehicle, and in what role).

Populating logic lives in database_populate_main.py. Rows reference vehicles
by vehicle_name and characters by character_name; ids are resolved at insert time.
"""

WIKI = "https://spaceballs.fandom.com/wiki/"
WIKIPEDIA = "https://en.wikipedia.org/wiki/Spaceballs"

VEHICLE_CREW = [
    # --- Eagle 5 ---
    {"vehicle_name": "Eagle 5", "character_name": "Lone Starr",
     "crew_role": "Captain"},  # WIKI + "Lone_Starr"
    {"vehicle_name": "Eagle 5", "character_name": "Barf",
     "crew_role": "Co-pilot"},  # WIKI + "Barf"

    # --- Honeymoon Cruise ---
    {"vehicle_name": "Honeymoon Cruise", "character_name": "Vespa",
     "crew_role": "Owner"},  # WIKI + "Honeymoon_Cruise", "her luxury Mercedes"
    {"vehicle_name": "Honeymoon Cruise", "character_name": "Dot Matrix",
     "crew_role": "Passenger"},  # WIKI + "Dot_Matrix", "dragged along for the ride"

    # --- Spaceball One ---
    {"vehicle_name": "Spaceball One", "character_name": "Dark Helmet",
     "crew_role": "Commander"},  # WIKI + "Spaceball_I"
    {"vehicle_name": "Spaceball One", "character_name": "Sandurz",
     "crew_role": "Commander under Dark Helmet"},  # WIKI + "Sandurz"
    {"vehicle_name": "Spaceball One", "character_name": "Rico",
     "crew_role": "Radio operator"},  # WIKI + "Rico"
    {"vehicle_name": "Spaceball One", "character_name": "Radar technician",
     "crew_role": "Radar technician"},  # WIKI + "Radar_Technician"
    {"vehicle_name": "Spaceball One", "character_name": "Major Asshole",
     "crew_role": "Officer"},  # WIKI + "Major_Asshole"
    {"vehicle_name": "Spaceball One", "character_name": "Phillip Asshole",
     "crew_role": "Gunner's Mate First Class"},  # WIKI + "Phillip_Asshole"
    {"vehicle_name": "Spaceball One", "character_name": "Kafka",
     "crew_role": "Technician (metamorphosis into Mega Maid)"},  # WIKI + "Kafka"
]
