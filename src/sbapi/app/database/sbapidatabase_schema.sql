/*
    This file contains the SQL schema for the Space Balls API database.
    It defines the structure of the tables and their relationships.
*/

/*
Character Table(s):
- characters: Stores information about characters.
- character_actors: Stores information about actors who played the characters.
- character_quotes: Stores quotes associated with characters.
- character_trivia: Stores trivia related to characters.
- character_behind_the_scenes: Stores behind-the-scenes notes for characters.
- character_references: Stores references and citations for character information.
*/

CREATE TABLE IF NOT EXISTS characters (
    id SERIAL PRIMARY KEY,
    character_name VARCHAR NOT NULL,
    full_name VARCHAR,
    species VARCHAR,
    gender VARCHAR,
    character_role VARCHAR,
    image_url VARCHAR,
    source_url VARCHAR,
    last_updated TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS character_actors (
    id SERIAL PRIMARY KEY,
    character_id INTEGER NOT NULL REFERENCES characters (id) ON DELETE CASCADE,
    actor_name VARCHAR NOT NULL,
    medium VARCHAR,
    notes TEXT
);

CREATE INDEX IF NOT EXISTS 
idx_character_actors_character_id ON character_actors (character_id);

CREATE TABLE IF NOT EXISTS character_quotes (
    id SERIAL PRIMARY KEY,
    character_id INTEGER NOT NULL REFERENCES characters (id) ON DELETE CASCADE,
    quote_text TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_character_quotes_character_id ON character_quotes (character_id);

CREATE TABLE IF NOT EXISTS character_trivia (
    id SERIAL PRIMARY KEY,
    character_id INTEGER NOT NULL REFERENCES characters (id) ON DELETE CASCADE,
    trivia_text TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_character_trivia_character_id ON character_trivia (character_id);

CREATE TABLE IF NOT EXISTS character_behind_the_scenes (
    id SERIAL PRIMARY KEY,
    character_id INTEGER NOT NULL REFERENCES characters (id) ON DELETE CASCADE,
    note_text TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_character_behind_the_scenes_character_id ON character_behind_the_scenes (character_id);

CREATE TABLE IF NOT EXISTS character_references (
    id SERIAL PRIMARY KEY,
    character_id INTEGER NOT NULL REFERENCES characters (id) ON DELETE CASCADE,
    citation_number INTEGER NOT NULL,
    source_text TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_character_references_character_id ON character_references (character_id);

/*
Location Table(s):
- locations: Stores information about locations (planets, ships, etc.).
- location_features: Stores notable features tied to a location.
- location_exports: Stores products/resources a location exports.
- location_relations: Stores relationships between locations (e.g. adjacency, conflict).
- location_trivia: Stores trivia related to locations.
- location_references: Stores references and citations for location information.
*/

CREATE TABLE IF NOT EXISTS locations (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    location_type VARCHAR,
    description TEXT,
    ruler_id INTEGER REFERENCES characters (id) ON DELETE SET NULL,
    heir_id INTEGER REFERENCES characters (id) ON DELETE SET NULL,
    image_url VARCHAR,
    source_url VARCHAR,
    last_updated TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_locations_ruler_id ON locations (ruler_id);
CREATE INDEX IF NOT EXISTS idx_locations_heir_id ON locations (heir_id);

CREATE TABLE IF NOT EXISTS location_features (
    id SERIAL PRIMARY KEY,
    location_id INTEGER NOT NULL REFERENCES locations (id) ON DELETE CASCADE,
    feature_name VARCHAR NOT NULL,
    feature_description TEXT
);

CREATE INDEX IF NOT EXISTS idx_location_features_location_id ON location_features (location_id);

CREATE TABLE IF NOT EXISTS location_exports (
    id SERIAL PRIMARY KEY,
    location_id INTEGER NOT NULL REFERENCES locations (id) ON DELETE CASCADE,
    product_name VARCHAR NOT NULL,
    notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_location_exports_location_id ON location_exports (location_id);

CREATE TABLE IF NOT EXISTS location_relations (
    id SERIAL PRIMARY KEY,
    location_id INTEGER NOT NULL REFERENCES locations (id) ON DELETE CASCADE,
    related_location_id INTEGER NOT NULL REFERENCES locations (id) ON DELETE CASCADE,
    relationship_type VARCHAR NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_location_relations_location_id ON location_relations (location_id);
CREATE INDEX IF NOT EXISTS idx_location_relations_related_location_id ON location_relations (related_location_id);

CREATE TABLE IF NOT EXISTS location_trivia (
    id SERIAL PRIMARY KEY,
    location_id INTEGER NOT NULL REFERENCES locations (id) ON DELETE CASCADE,
    trivia_text TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_location_trivia_location_id ON location_trivia (location_id);

CREATE TABLE IF NOT EXISTS location_references (
    id SERIAL PRIMARY KEY,
    location_id INTEGER NOT NULL REFERENCES locations (id) ON DELETE CASCADE,
    citation_number INTEGER NOT NULL,
    source_text TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_location_references_location_id ON location_references (location_id);

/*
Faction Table(s):
- factions: Stores information about organisations/factions (Spaceballs empire, Druidia, Yogurt's order).
- faction_trivia: Stores trivia related to factions.
- faction_references: Stores references and citations for faction information.
*/

CREATE TABLE IF NOT EXISTS factions (
    id SERIAL PRIMARY KEY,
    faction_name VARCHAR NOT NULL,
    description TEXT,
    leader_id INTEGER REFERENCES characters (id) ON DELETE SET NULL,
    image_url VARCHAR,
    source_url VARCHAR,
    last_updated TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_factions_leader_id ON factions (leader_id);

ALTER TABLE characters ADD COLUMN IF NOT EXISTS faction_id INTEGER REFERENCES factions (id) ON DELETE SET NULL;

CREATE INDEX IF NOT EXISTS idx_characters_faction_id ON characters (faction_id);

CREATE TABLE IF NOT EXISTS faction_trivia (
    id SERIAL PRIMARY KEY,
    faction_id INTEGER NOT NULL REFERENCES factions (id) ON DELETE CASCADE,
    trivia_text TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_faction_trivia_faction_id ON faction_trivia (faction_id);

CREATE TABLE IF NOT EXISTS faction_references (
    id SERIAL PRIMARY KEY,
    faction_id INTEGER NOT NULL REFERENCES factions (id) ON DELETE CASCADE,
    citation_number INTEGER NOT NULL,
    source_text TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_faction_references_faction_id ON faction_references (faction_id);

/*
Vehicle Table(s):
- vehicles: Stores information about spacecraft/vehicles (Eagle 5, Spaceball One, Winnebago).
- vehicle_trivia: Stores trivia related to vehicles.
- vehicle_references: Stores references and citations for vehicle information.
*/

CREATE TABLE IF NOT EXISTS vehicles (
    id SERIAL PRIMARY KEY,
    vehicle_name VARCHAR NOT NULL,
    vehicle_type VARCHAR,
    description TEXT,
    pilot_id INTEGER REFERENCES characters (id) ON DELETE SET NULL,
    faction_id INTEGER REFERENCES factions (id) ON DELETE SET NULL,
    image_url VARCHAR,
    source_url VARCHAR,
    last_updated TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_vehicles_pilot_id ON vehicles (pilot_id);
CREATE INDEX IF NOT EXISTS idx_vehicles_faction_id ON vehicles (faction_id);

CREATE TABLE IF NOT EXISTS vehicle_trivia (
    id SERIAL PRIMARY KEY,
    vehicle_id INTEGER NOT NULL REFERENCES vehicles (id) ON DELETE CASCADE,
    trivia_text TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_vehicle_trivia_vehicle_id ON vehicle_trivia (vehicle_id);

CREATE TABLE IF NOT EXISTS vehicle_references (
    id SERIAL PRIMARY KEY,
    vehicle_id INTEGER NOT NULL REFERENCES vehicles (id) ON DELETE CASCADE,
    citation_number INTEGER NOT NULL,
    source_text TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_vehicle_references_vehicle_id ON vehicle_references (vehicle_id);

/*
Item Table(s):
- items: Stores information about objects (The Schwartz, the ring, merchandise, air canisters).
  Kept as a single table with an item_type column rather than split into weapons/technology/etc,
  since the source material doesn't separate those categories.
- item_trivia: Stores trivia related to items.
- item_references: Stores references and citations for item information.
*/

CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR NOT NULL,
    item_type VARCHAR NOT NULL
        CHECK (item_type IN ('weapon', 'artifact', 'tech', 'merchandise', 'other')),
    description TEXT,
    owner_character_id INTEGER REFERENCES characters (id) ON DELETE SET NULL,
    image_url VARCHAR,
    source_url VARCHAR,
    last_updated TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_items_owner_character_id ON items (owner_character_id);

CREATE TABLE IF NOT EXISTS item_trivia (
    id SERIAL PRIMARY KEY,
    item_id INTEGER NOT NULL REFERENCES items (id) ON DELETE CASCADE,
    trivia_text TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_item_trivia_item_id ON item_trivia (item_id);

CREATE TABLE IF NOT EXISTS item_references (
    id SERIAL PRIMARY KEY,
    item_id INTEGER NOT NULL REFERENCES items (id) ON DELETE CASCADE,
    citation_number INTEGER NOT NULL,
    source_text TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_item_references_item_id ON item_references (item_id);

/*
Media Table(s):
- media: Stores one row per film/show (Spaceballs, Spaceballs 2, Animated Series).
- episodes: Stores episodes belonging to a media entry (e.g. Animated Series).
- episode_references: Stores references and citations for episode information.
- media_trivia: Stores trivia related to media entries.
- media_references: Stores references and citations for media information.
*/

CREATE TABLE IF NOT EXISTS media (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    media_type VARCHAR,
    release_date DATE,
    description TEXT,
    image_url VARCHAR,
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
    source_url VARCHAR,
    last_updated TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_episodes_media_id ON episodes (media_id);

CREATE TABLE IF NOT EXISTS episode_references (
    id SERIAL PRIMARY KEY,
    episode_id INTEGER NOT NULL REFERENCES episodes (id) ON DELETE CASCADE,
    citation_number INTEGER NOT NULL,
    source_text TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_episode_references_episode_id ON episode_references (episode_id);

CREATE TABLE IF NOT EXISTS media_trivia (
    id SERIAL PRIMARY KEY,
    media_id INTEGER NOT NULL REFERENCES media (id) ON DELETE CASCADE,
    trivia_text TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_media_trivia_media_id ON media_trivia (media_id);

CREATE TABLE IF NOT EXISTS media_references (
    id SERIAL PRIMARY KEY,
    media_id INTEGER NOT NULL REFERENCES media (id) ON DELETE CASCADE,
    citation_number INTEGER NOT NULL,
    source_text TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_media_references_media_id ON media_references (media_id);

/*
Actor Table(s):
- actors: Stores real-world cast members.
- actor_references: Stores references and citations for actor information.
- character_actors: Join table linking a character to the actor(s) who played them,
  per media entry (handles an actor playing a role across multiple entries).
  Replaces the earlier character_actors table that stored actor_name inline.
*/

DROP TABLE IF EXISTS character_actors;

CREATE TABLE IF NOT EXISTS actors (
    id SERIAL PRIMARY KEY,
    actor_name VARCHAR NOT NULL,
    image_url VARCHAR,
    source_url VARCHAR,
    last_updated TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS actor_references (
    id SERIAL PRIMARY KEY,
    actor_id INTEGER NOT NULL REFERENCES actors (id) ON DELETE CASCADE,
    citation_number INTEGER NOT NULL,
    source_text TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_actor_references_actor_id ON actor_references (actor_id);

CREATE TABLE IF NOT EXISTS character_actors (
    id SERIAL PRIMARY KEY,
    character_id INTEGER NOT NULL REFERENCES characters (id) ON DELETE CASCADE,
    actor_id INTEGER NOT NULL REFERENCES actors (id) ON DELETE CASCADE,
    media_id INTEGER REFERENCES media (id) ON DELETE SET NULL,
    notes TEXT,
    UNIQUE (character_id, actor_id, media_id)
);

CREATE INDEX IF NOT EXISTS idx_character_actors_character_id ON character_actors (character_id);
CREATE INDEX IF NOT EXISTS idx_character_actors_actor_id ON character_actors (actor_id);
CREATE INDEX IF NOT EXISTS idx_character_actors_media_id ON character_actors (media_id);

/*
Quote linkage:
- character_quotes already stores per-character quotes; add an optional media_id
  so a quote can be tied to the specific film/episode it's from, instead of
  introducing a separate, overlapping quotes table.
*/

ALTER TABLE character_quotes ADD COLUMN IF NOT EXISTS media_id INTEGER REFERENCES media (id) ON DELETE SET NULL;

CREATE INDEX IF NOT EXISTS idx_character_quotes_media_id ON character_quotes (media_id);
