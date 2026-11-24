"""
Data for the quotes table (verbatim lines from the 1987 film).

Populating logic lives in database_populate_main.py. Speakers are referenced by
character_name and resolved to an id at insert time.
"""

from datetime import UTC, datetime

NOW = datetime.now(UTC)

WIKI = "https://spaceballs.fandom.com/wiki/"
WIKIQUOTE = "https://en.wikiquote.org/wiki/Spaceballs"

QUOTES = [
    # --- Heroes ---
    {
        "quote_text": "On this ship you're to refer to me as 'idiot,' not "
        "'you Captain.' I mean... you know what I mean.",
        "character_name": "Lone Starr",
        "source_url": WIKI + "Lone_Starr",
        "last_updated": NOW,
    },
    {
        "quote_text": "A hundred thousand spacebucks!?",
        "character_name": "Lone Starr",
        "source_url": WIKI + "Spacebucks",
        "last_updated": NOW,
    },
    {
        "quote_text": "We got a minute and forty before the end of the world. Hang on.",
        "character_name": "Lone Starr",
        "source_url": WIKI + "Self-destruct_button",
        "last_updated": NOW,
    },
    {
        "quote_text": "Did I miss something? When did we get to Disneyland?",
        "character_name": "Lone Starr",
        "source_url": WIKIQUOTE,
        "last_updated": NOW,
    },
    {
        "quote_text": "I'm a mawg: half-man, half-dog. I'm my own best friend.",
        "character_name": "Barf",
        "source_url": WIKI + "Mawg",
        "last_updated": NOW,
    },
    {
        "quote_text": "Funny, she doesn't look Druish.",
        "character_name": "Barf",
        "source_url": WIKI + "Barf",
        "last_updated": NOW,
    },
    {
        "quote_text": "They've gone to plaid!",
        "character_name": "Barf",
        "source_url": WIKI + "Ludicrous_Speed",
        "last_updated": NOW,
    },
    {
        "quote_text": "Wow! Liquid Schwartz!",
        "character_name": "Barf",
        "source_url": WIKI + "Liquid_Schwartz",
        "last_updated": NOW,
    },
    {
        "quote_text": "I am Princess Vespa, daughter of Roland, King of the Druids.",
        "character_name": "Vespa",
        "source_url": WIKI + "Vespa",
        "last_updated": NOW,
    },
    {
        "quote_text": "That was my Virgin Alarm. It's programmed to go off "
        "before you do.",
        "character_name": "Dot Matrix",
        "source_url": WIKI + "Virgin_Alarm",
        "last_updated": NOW,
    },
    {
        "quote_text": "Please, please, don't make a fuss. I'm just plain Yogurt.",
        "character_name": "Yogurt",
        "source_url": WIKI + "Yogurt",
        "last_updated": NOW,
    },
    # --- Druidia ---
    {
        "quote_text": "Oh, and, if at all possible, try to save the car.",
        "character_name": "Roland",
        "source_url": WIKI + "Roland",
        "last_updated": NOW,
    },
    # --- Spaceballs ---
    {
        "quote_text": "I can't make decisions, I'm a president!",
        "character_name": "Skroob",
        "source_url": WIKI + "Skroob",
        "last_updated": NOW,
    },
    {
        "quote_text": "1, 2, 3, 4, 5? That's amazing! I've got the same "
        "combination on my luggage!",
        "character_name": "Skroob",
        "source_url": WIKIQUOTE,
        "last_updated": NOW,
    },
    {
        "quote_text": "Why didn't somebody tell me my ass was so big?!",
        "character_name": "Skroob",
        "source_url": WIKIQUOTE,
        "last_updated": NOW,
    },
    {
        "quote_text": "What? You went over my helmet!?",
        "character_name": "Dark Helmet",
        "source_url": WIKI + "Dark_Helmet",
        "last_updated": NOW,
    },
    {
        "quote_text": "Keep firing, Assholes!",
        "character_name": "Dark Helmet",
        "source_url": WIKI + "Asshole",
        "last_updated": NOW,
    },
    {
        "quote_text": "That's the stupidest combination I've ever heard in my life!",
        "character_name": "Dark Helmet",
        "source_url": WIKI + "Air_shield",
        "last_updated": NOW,
    },
    {
        "quote_text": "Ludicrous Speed, Go!",
        "character_name": "Dark Helmet",
        "source_url": WIKIQUOTE,
        "last_updated": NOW,
    },
    {
        "quote_text": "Smoke if you got 'em.",
        "character_name": "Dark Helmet",
        "source_url": WIKI + "Ludicrous_Speed",
        "last_updated": NOW,
    },
    {
        "quote_text": "You have the ring. And I see your Schwartz is as big as "
        "mine. Now, let's see how well you handle it.",
        "character_name": "Dark Helmet",
        "source_url": WIKIQUOTE,
        "last_updated": NOW,
    },
    {
        "quote_text": "So, Lone Starr, now you see that evil will always "
        "triumph, because good is dumb.",
        "character_name": "Dark Helmet",
        "source_url": WIKIQUOTE,
        "last_updated": NOW,
    },
    {
        "quote_text": "Attention! This is Colonel Sandurz in forward command! "
        "Abandon ship! Abandon ship!",
        "character_name": "Sandurz",
        "source_url": WIKI + "Sandurz",
        "last_updated": NOW,
    },
    {
        "quote_text": "I did sir. He's my cousin.",
        "character_name": "Major Asshole",
        "source_url": WIKI + "Major_Asshole",
        "last_updated": NOW,
    },
    {
        "quote_text": "I'm sorry sir, I'm doing my best.",
        "character_name": "Phillip Asshole",
        "source_url": WIKI + "Phillip_Asshole",
        "last_updated": NOW,
    },
    {
        "quote_text": "You idiots! These are not them! You've captured their "
        "stunt doubles!",
        "character_name": "Captain of the Guard",
        "source_url": WIKI + "Captain_of_the_Guard",
        "last_updated": NOW,
    },
    {
        "quote_text": "We ain't found shit!",
        "character_name": "Trooper with comb",
        "source_url": WIKI + "Trooper_with_Comb",
        "last_updated": NOW,
    },
    {
        "quote_text": "20 Seconds remaining. This is your last chance to press "
        "the cancellation button.",
        "character_name": None,  # Mega Maid's computer voice, no character row
        "source_url": WIKI + "Mega_Maid",
        "last_updated": NOW,
    },
    # --- Underworld ---
    {
        "quote_text": "It's not what I want. It's what he wants.",
        "character_name": "Vinnie",
        "source_url": WIKI + "Vinnie",
        "last_updated": NOW,
    },
    {
        "quote_text": "You're delicious",
        "character_name": "Vinnie",
        "source_url": WIKI + "Pizza_the_Hutt",
        "last_updated": NOW,
    },
]
