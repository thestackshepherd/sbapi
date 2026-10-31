/*
    This file contains the SQL schema for the Space Balls API database.

    One table per kind of thing, and everything about a thing lives on its row:
    media, episodes, actors, factions, locations, characters, vehicles, items, quotes.

    - Single links (a character's faction or homeworld, a vehicle's faction) are
      plain foreign-key columns.
    - Lists are plain TEXT[] columns on the row instead of join tables:
        appears_in         titles of the media entries it appears in
        actors, voice_actors   (characters) who played / voiced them
        crew               (vehicles) names of the characters aboard
        trivia, behind_the_scenes   notes
        citations          the page's references, in order (link in parentheses)

    Every descriptive column is nullable on purpose: values are only filled in
    when they can be sourced (see CLAUDE.md).
*/

/*
Media Table(s):
- media: Stores one row per film/show (Spaceballs, Spaceballs: The Animated Series).
- episodes: Stores episodes belonging to a media entry (e.g. the Animated Series).
*/

CREATE TABLE IF NOT EXISTS media (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    media_type VARCHAR
        CHECK (media_type IN ('film', 'series')),
    release_date DATE,
    description TEXT,
    image_url VARCHAR,
    trivia TEXT[] NOT NULL DEFAULT '{}',
    behind_the_scenes TEXT[] NOT NULL DEFAULT '{}',
    citations TEXT[] NOT NULL DEFAULT '{}',
    source_url VARCHAR,
    last_updated TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS episodes (
    id SERIAL PRIMARY KEY,
    media_id INTEGER NOT NULL REFERENCES media (id) ON DELETE CASCADE,
    season_number INTEGER,
    episode_number INTEGER,
    title VARCHAR NOT NULL,
    description TEXT,
    air_date DATE,
    trivia TEXT[] NOT NULL DEFAULT '{}',
    behind_the_scenes TEXT[] NOT NULL DEFAULT '{}',
    citations TEXT[] NOT NULL DEFAULT '{}',
    source_url VARCHAR,
    last_updated TIMESTAMPTZ,
    UNIQUE (media_id, season_number, episode_number)
);

CREATE INDEX IF NOT EXISTS idx_episodes_media_id ON episodes (media_id);

/*
Actor Table(s):
- actors: Stores real-world cast members.
*/

CREATE TABLE IF NOT EXISTS actors (
    id SERIAL PRIMARY KEY,
    actor_name VARCHAR NOT NULL,
    image_url VARCHAR,
    trivia TEXT[] NOT NULL DEFAULT '{}',
    behind_the_scenes TEXT[] NOT NULL DEFAULT '{}',
    citations TEXT[] NOT NULL DEFAULT '{}',
    source_url VARCHAR,
    last_updated TIMESTAMPTZ
);

/*
Faction Table(s):
- factions: Stores organisations/factions (Spaceballs, Druidia's royal house, Yogurt's order).
  leader_id is added after characters exists, since the two tables reference each other.
*/

CREATE TABLE IF NOT EXISTS factions (
    id SERIAL PRIMARY KEY,
    faction_name VARCHAR NOT NULL,
    description TEXT,
    parody_of VARCHAR,
    image_url VARCHAR,
    trivia TEXT[] NOT NULL DEFAULT '{}',
    behind_the_scenes TEXT[] NOT NULL DEFAULT '{}',
    citations TEXT[] NOT NULL DEFAULT '{}',
    source_url VARCHAR,
    last_updated TIMESTAMPTZ
);

/*
Location Table(s):
- locations: Stores places (planets, moons, ships used as settings, etc.).
  ruler_id/heir_id are added after characters exists, since the two tables reference each other.
*/

CREATE TABLE IF NOT EXISTS locations (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    location_type VARCHAR,
    description TEXT,
    parody_of VARCHAR,
    image_url VARCHAR,
    appears_in TEXT[] NOT NULL DEFAULT '{}',
    trivia TEXT[] NOT NULL DEFAULT '{}',
    behind_the_scenes TEXT[] NOT NULL DEFAULT '{}',
    citations TEXT[] NOT NULL DEFAULT '{}',
    source_url VARCHAR,
    last_updated TIMESTAMPTZ
);

/*
Character Table(s):
- characters: Stores characters. parody_of names the character being spoofed
  (e.g. a Star Wars character), when sourced.
*/

CREATE TABLE IF NOT EXISTS characters (
    id SERIAL PRIMARY KEY,
    character_name VARCHAR NOT NULL,
    full_name VARCHAR,
    species VARCHAR,
    gender VARCHAR,
    character_role VARCHAR,
    parody_of VARCHAR,
    faction_id INTEGER REFERENCES factions (id) ON DELETE SET NULL,
    homeworld_id INTEGER REFERENCES locations (id) ON DELETE SET NULL,
    image_url VARCHAR,
    appears_in TEXT[] NOT NULL DEFAULT '{}',
    actors TEXT[] NOT NULL DEFAULT '{}',
    voice_actors TEXT[] NOT NULL DEFAULT '{}',
    trivia TEXT[] NOT NULL DEFAULT '{}',
    behind_the_scenes TEXT[] NOT NULL DEFAULT '{}',
    citations TEXT[] NOT NULL DEFAULT '{}',
    source_url VARCHAR,
    last_updated TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_characters_faction_id ON characters (faction_id);
CREATE INDEX IF NOT EXISTS idx_characters_homeworld_id ON characters (homeworld_id);

ALTER TABLE factions ADD COLUMN IF NOT EXISTS leader_id INTEGER REFERENCES characters (id) ON DELETE SET NULL;

CREATE INDEX IF NOT EXISTS idx_factions_leader_id ON factions (leader_id);

ALTER TABLE locations ADD COLUMN IF NOT EXISTS ruler_id INTEGER REFERENCES characters (id) ON DELETE SET NULL;
ALTER TABLE locations ADD COLUMN IF NOT EXISTS heir_id INTEGER REFERENCES characters (id) ON DELETE SET NULL;

CREATE INDEX IF NOT EXISTS idx_locations_ruler_id ON locations (ruler_id);
CREATE INDEX IF NOT EXISTS idx_locations_heir_id ON locations (heir_id);

/*
Vehicle Table(s):
- vehicles: Stores spacecraft/vehicles (Eagle 5, Spaceball One).
  Who is aboard, and in what role, is the crew column (most have more than one person).
*/

CREATE TABLE IF NOT EXISTS vehicles (
    id SERIAL PRIMARY KEY,
    vehicle_name VARCHAR NOT NULL,
    vehicle_type VARCHAR,
    description TEXT,
    parody_of VARCHAR,
    faction_id INTEGER REFERENCES factions (id) ON DELETE SET NULL,
    image_url VARCHAR,
    appears_in TEXT[] NOT NULL DEFAULT '{}',
    crew TEXT[] NOT NULL DEFAULT '{}',
    trivia TEXT[] NOT NULL DEFAULT '{}',
    behind_the_scenes TEXT[] NOT NULL DEFAULT '{}',
    citations TEXT[] NOT NULL DEFAULT '{}',
    source_url VARCHAR,
    last_updated TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_vehicles_faction_id ON vehicles (faction_id);

/*
Item Table(s):
- items: Stores objects (The Schwartz, the ring, merchandise, air canisters).
  Kept as a single table with an item_type column rather than split into weapons/technology/etc,
  since the source material doesn't separate those categories.
*/

CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR NOT NULL,
    item_type VARCHAR NOT NULL
        CHECK (item_type IN ('weapon', 'artifact', 'tech', 'merchandise', 'other')),
    description TEXT,
    parody_of VARCHAR,
    owner_character_id INTEGER REFERENCES characters (id) ON DELETE SET NULL,
    image_url VARCHAR,
    trivia TEXT[] NOT NULL DEFAULT '{}',
    behind_the_scenes TEXT[] NOT NULL DEFAULT '{}',
    citations TEXT[] NOT NULL DEFAULT '{}',
    source_url VARCHAR,
    last_updated TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_items_owner_character_id ON items (owner_character_id);

/*
Quote Table(s):
- quotes: Stores lines of dialogue. character_id is nullable for lines whose speaker
  can't be sourced; media_id/episode_id tie a line to where it is spoken.
*/

CREATE TABLE IF NOT EXISTS quotes (
    id SERIAL PRIMARY KEY,
    quote_text TEXT NOT NULL,
    character_id INTEGER REFERENCES characters (id) ON DELETE SET NULL,
    media_id INTEGER REFERENCES media (id) ON DELETE SET NULL,
    episode_id INTEGER REFERENCES episodes (id) ON DELETE SET NULL,
    citations TEXT[] NOT NULL DEFAULT '{}',
    source_url VARCHAR,
    last_updated TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_quotes_character_id ON quotes (character_id);
CREATE INDEX IF NOT EXISTS idx_quotes_media_id ON quotes (media_id);
CREATE INDEX IF NOT EXISTS idx_quotes_episode_id ON quotes (episode_id);
