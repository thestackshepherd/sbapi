"""
Data for the trivia table (trivia and behind-the-scenes notes).

Populating logic lives in database_populate_main.py. Each row names exactly one
entity by its natural key (character_name, planet_name, vehicle_name,
item_name, or actor_name), resolved to an id at insert time. The trivia table
has no source column, so each group notes the page the text was taken from.
"""

WIKI = "https://spaceballs.fandom.com/wiki/"

TRIVIA = [
    # --- Vehicles ---
    # WIKI + "Eagle_5"
    {
        "trivia_kind": "trivia",
        "vehicle_name": "Eagle 5",
        "trivia_text": "The Eagle 5 is a 1986 Winnebago Chieftain 33.",
    },
    {
        "trivia_kind": "trivia",
        "vehicle_name": "Eagle 5",
        "trivia_text": "Despite the Eagle 5 being a motorhome, Lone Starr repeatedly "
        "refers to it as a ship.",
    },
    {
        "trivia_kind": "behind_the_scenes",
        "vehicle_name": "Eagle 5",
        "trivia_text": "In 2017, the original 1/12th scale model of the Eagle 5 used "
        "in filming was put on auction. It was reportedly sold in June of that year "
        "for $28,000.",
    },
    # WIKI + "Spaceball_I"
    {
        "trivia_kind": "trivia",
        "vehicle_name": "Spaceball One",
        "trivia_text": "It takes almost two minutes for the camera to finish panning "
        "across Spaceball One.",
    },
    {
        "trivia_kind": "trivia",
        "vehicle_name": "Spaceball One",
        "trivia_text": "In Spaceballs: The Animated Series, the ship has the slightly "
        "different name of Spaceballs I.",
    },
    # WIKI + "Ludicrous_Speed"
    {
        "trivia_kind": "trivia",
        "vehicle_name": "Spaceball One",
        "trivia_text": "When recovering from Ludicrous Speed, Dark Helmet suggests "
        "the crew take a five-minute break. The next time we see them in the film "
        "is in fact five minutes later.",
    },
    # WIKI + "Mega_Maid"
    {
        "trivia_kind": "trivia",
        "vehicle_name": "Mega Maid",
        "trivia_text": "Dark Helmet calls the Spaceball in charge of the "
        '"metamorphosis" of Spaceball One into Mega Maid "Kafka", a reference '
        "to Franz Kafka, author of The Metamorphosis.",
    },
    # --- Items ---
    # WIKI + "Schwartz-ring"
    {
        "trivia_kind": "behind_the_scenes",
        "item_name": "Ring of the Schwartz",
        "trivia_text": "Due to a technical goof, the Schwartz ring reappears on Lone "
        "Starr's finger after he and the other heroes escape Spaceball One.",
    },
    # WIKI + "Mr._Rental"
    {
        "trivia_kind": "trivia",
        "item_name": "Mr. Rental",
        "trivia_text": "Mr. Rental is mostly stocked with older Mel Brooks films, "
        "including The Producers, Blazing Saddles, and Young Frankenstein, plus "
        "Rocky I through XIV.",
    },
    # WIKI + "Spaceballs:_The..."
    {
        "trivia_kind": "behind_the_scenes",
        "item_name": "Spaceballs: The Coloring Book",
        "trivia_text": "The coloring book is actually a Transformers product with "
        "the Spaceballs logo slapped on.",
    },
    {
        "trivia_kind": "behind_the_scenes",
        "item_name": "Spaceballs: The Lunchbox",
        "trivia_text": "The lunchbox is actually a Transformers product with the "
        "Spaceballs logo slapped on.",
    },
    # --- Characters ---
    # WIKI + "Lone_Starr"
    {
        "trivia_kind": "behind_the_scenes",
        "character_name": "Lone Starr",
        "trivia_text": "Bill Pullman was the third choice for Lone Starr, behind "
        "Tom Cruise and Tom Hanks.",
    },
    # WIKI + "Barf"
    {
        "trivia_kind": "behind_the_scenes",
        "character_name": "Barf",
        "trivia_text": "Rick Moranis suggested John Candy for the role of Barf.",
    },
    {
        "trivia_kind": "behind_the_scenes",
        "character_name": "Barf",
        "trivia_text": "Barf forgetting to unbuckle his seat belt (\"Oh! That's "
        'gonna leave a mark.") was a gag John Candy performed on the spot.',
    },
    # WIKI + "Yogurt"
    {
        "trivia_kind": "behind_the_scenes",
        "character_name": "Yogurt",
        "trivia_text": "The gold-colored make-up gave Mel Brooks a rash on his face "
        "and neck, so most of Yogurt's scenes were shot out of sequence.",
    },
    {
        "trivia_kind": "behind_the_scenes",
        "character_name": "Yogurt",
        "trivia_text": "The scenes in Yogurt's temple were filmed on the same "
        "soundstage where MGM shot the Wizard of Oz scenes in the 1930s.",
    },
    # WIKI + "Skroob"
    {
        "trivia_kind": "trivia",
        "character_name": "Skroob",
        "trivia_text": "President Skroob's last name is an anagram of Mel Brooks' "
        "last name.",
    },
    # WIKI + "Dark_Helmet"
    {
        "trivia_kind": "behind_the_scenes",
        "character_name": "Dark Helmet",
        "trivia_text": "The scene of Dark Helmet playing with his dolls was not in "
        "the screenplay; Rick Moranis improvised the entire scene.",
    },
    {
        "trivia_kind": "trivia",
        "character_name": "Dark Helmet",
        "trivia_text": "Dark Helmet lowers his voice when closing his mask and "
        "speaks at a normal tone after opening it, which Rick Moranis decided to do.",
    },
    # WIKI + "Sandurz"
    {
        "trivia_kind": "trivia",
        "character_name": "Sandurz",
        "trivia_text": "Colonel Sandurz's name is a pun on Colonel Sanders, which "
        'is lampshaded when Dark Helmet calls him a "chicken."',
    },
    # WIKI + "Prince_Valium"
    {
        "trivia_kind": "trivia",
        "character_name": "Valium",
        "trivia_text": "Prince Valium is a play on the prescription sleep aid of "
        "the same name, which is why he can't stay awake.",
    },
    # WIKI + "Radar_Technician"
    {
        "trivia_kind": "behind_the_scenes",
        "character_name": "Radar technician",
        "trivia_text": "Michael Winslow made each of the radar sounds in his scene "
        "himself.",
    },
    # WIKI + "Pizza_the_Hutt"
    {
        "trivia_kind": "behind_the_scenes",
        "character_name": "Pizza the Hutt",
        "trivia_text": "The Pizza the Hutt costume used pancake batter, not real "
        "cheese, but it did use real pepperoni.",
    },
    # WIKI + "Vinnie"
    {
        "trivia_kind": "behind_the_scenes",
        "character_name": "Vinnie",
        "trivia_text": "The name was inspired by Rudy DeLuca's brother, Vincent "
        "Thomas DeLuca.",
    },
    # --- Planets ---
    # WIKI + "Druidia"
    {
        "trivia_kind": "trivia",
        "planet_name": "Planet Druidia",
        "trivia_text": 'Mel Brooks chose the name "Druidia" to set up the gag in '
        'which Lone Starr calls Vespa a "Druish Princess".',
    },
    {
        "trivia_kind": "behind_the_scenes",
        "planet_name": "Planet Druidia",
        "trivia_text": "The castle on Druidia is Neuschwanstein Castle in Bavaria, "
        "modified by matte painting with additional ramps.",
    },
    # WIKI + "Moon_of_Vega"
    {
        "trivia_kind": "trivia",
        "planet_name": "Moon of Vega",
        "trivia_text": "Music from Lawrence of Arabia plays while the gang crosses "
        "the sand dunes.",
    },
    # --- Actors ---
    # WIKI + "Spaceballs"
    {
        "trivia_kind": "behind_the_scenes",
        "actor_name": "John Hurt",
        "trivia_text": "John Hurt said Mel Brooks talked him into parodying his "
        "role from Alien by making it sound like a brief walk-on cameo.",
    },
    {
        "trivia_kind": "behind_the_scenes",
        "actor_name": "Mel Brooks",
        "trivia_text": "Mel Brooks says the two jokes he is most proud of are the "
        'merchandising running gag and Colonel Sandurz renting "Spaceballs" '
        "before it was finished.",
    },
    # WIKI + "Minister"
    {
        "trivia_kind": "trivia",
        "actor_name": "Ronny Graham",
        "trivia_text": "Ronny Graham, who plays the Minister, was one of the "
        "writers of the movie.",
    },
]
