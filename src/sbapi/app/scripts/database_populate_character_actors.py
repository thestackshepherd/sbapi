"""
Data for the character_actors table (which actor played or voiced which character).

Populating logic lives in database_populate_main.py. Rows reference characters
by character_name and actors by actor_name; ids are resolved at insert time.
"""

WIKI = "https://spaceballs.fandom.com/wiki/"
WIKIPEDIA = "https://en.wikipedia.org/wiki/Spaceballs"

# source for every row: the Cast section of WIKI + "Spaceballs", cross-checked
# against each character's infobox and the Cast section of WIKIPEDIA.
CHARACTER_ACTORS = [
    # --- Heroes ---
    {"character_name": "Lone Starr", "actor_name": "Bill Pullman",
     "credit_type": "live_action", "notes": None},
    {"character_name": "Barf", "actor_name": "John Candy",
     "credit_type": "live_action", "notes": None},
    {"character_name": "Vespa", "actor_name": "Daphne Zuniga",
     "credit_type": "live_action", "notes": None},
    {"character_name": "Dot Matrix", "actor_name": "Joan Rivers",
     "credit_type": "voice", "notes": None},
    {"character_name": "Dot Matrix", "actor_name": "Lorene Yarnell",
     "credit_type": "live_action", "notes": "On-screen physical performance (body)"},
    {"character_name": "Yogurt", "actor_name": "Mel Brooks",
     "credit_type": "live_action", "notes": "Mel Brooks also plays Skroob"},

    # --- Druidia ---
    {"character_name": "Roland", "actor_name": "Dick Van Patten",
     "credit_type": "live_action", "notes": None},
    {"character_name": "Valium", "actor_name": "Jm J. Bullock",
     "credit_type": "live_action", "notes": None},
    {"character_name": "Minister", "actor_name": "Ronny Graham",
     "credit_type": "live_action", "notes": None},

    # --- Spaceballs ---
    {"character_name": "Skroob", "actor_name": "Mel Brooks",
     "credit_type": "live_action", "notes": "Mel Brooks also plays Yogurt"},
    {"character_name": "Dark Helmet", "actor_name": "Rick Moranis",
     "credit_type": "live_action", "notes": None},
    {"character_name": "Sandurz", "actor_name": "George Wyner",
     "credit_type": "live_action", "notes": None},
    {"character_name": "Rico", "actor_name": "Sal Viscuso",
     "credit_type": "live_action", "notes": "Credited as Radio Operator"},
    {"character_name": "Zircon", "actor_name": "Leslie Bevis",
     "credit_type": "live_action", "notes": None},
    {"character_name": "Snotty", "actor_name": "Jeff MacGregor",
     "credit_type": "live_action", "notes": None},
    {"character_name": "Major Asshole", "actor_name": "Jim Jackman",
     "credit_type": "live_action", "notes": None},
    {"character_name": "Phillip Asshole", "actor_name": "Michael Pniewski",
     "credit_type": "live_action", "notes": "Credited as Laser Gunner"},
    {"character_name": "Radar technician", "actor_name": "Michael Winslow",
     "credit_type": "live_action", "notes": None},
    {"character_name": "Captain of the Guard", "actor_name": "Stephen Tobolowsky",
     "credit_type": "live_action", "notes": None},
    {"character_name": "Trooper with comb", "actor_name": "Tim Russ",
     "credit_type": "live_action", "notes": None},
    {"character_name": "Charlene", "actor_name": "Denise Gallup",
     "credit_type": "live_action", "notes": None},
    {"character_name": "Marlene", "actor_name": "Dian Gallup",
     "credit_type": "live_action", "notes": None},
    {"character_name": "Schlotkin", "actor_name": "Sandy Helberg",
     "credit_type": "live_action", "notes": None},

    # --- Underworld ---
    {"character_name": "Pizza the Hutt", "actor_name": "Dom DeLuise",
     "credit_type": "voice",
     "notes": "Richard Karron and Rick Lazzarini performed on screen"},
    {"character_name": "Vinnie", "actor_name": "Rudy DeLuca",
     "credit_type": "live_action", "notes": None},

    # --- Moon of Vega (the Dinks are one character row) ---
    {"character_name": "Dinks", "actor_name": "Ed Gale",
     "credit_type": "live_action", "notes": None},
    {"character_name": "Dinks", "actor_name": "Antonio Hoyos",
     "credit_type": "live_action", "notes": None},
    {"character_name": "Dinks", "actor_name": "Felix Silla",
     "credit_type": "live_action", "notes": None},
    {"character_name": "Dinks", "actor_name": "Arturo Gil",
     "credit_type": "live_action", "notes": None},
    {"character_name": "Dinks", "actor_name": "Tony Cox",
     "credit_type": "live_action", "notes": None},
    {"character_name": "Dinks", "actor_name": "John Kennedy Hayden",
     "credit_type": "live_action", "notes": None},

    # --- Cameos ---
    {"character_name": "Kane", "actor_name": "John Hurt",
     "credit_type": "live_action",
     "notes": "Cameo parodying his own role in Alien (1979)"},  # WIKIPEDIA
]
