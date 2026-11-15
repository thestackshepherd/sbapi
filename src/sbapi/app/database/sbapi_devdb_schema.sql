--- Space Balls API database schema ---------

--- Actor Tables ---------

--- actors: Stores real-world cast members. ---------
DROP TABLE IF EXISTS actors CASCADE;
CREATE TABLE actors (
    id            SERIAL  PRIMARY KEY,
    actor_name    VARCHAR UNIQUE NOT NULL,
    last_updated  TIMESTAMPTZ
);

--- Faction Tables ---------

--- factions: Stores the groups characters and vehicles belong to. ---------
DROP TABLE IF EXISTS factions CASCADE;
CREATE TABLE factions (
    id SERIAL PRIMARY KEY,
    faction_name VARCHAR NOT NULL,
    description TEXT,
    parody_of VARCHAR,
    image_url VARCHAR,
    source_url VARCHAR,
    last_updated TIMESTAMPTZ
);

--- Location Tables ---------

--- locations: Stores planets, moons, and other settings. ---------
DROP TABLE IF EXISTS locations CASCADE;
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    location_type VARCHAR,
    description TEXT,
    parody_of VARCHAR,
    image_url VARCHAR,
    source_url VARCHAR,
    last_updated TIMESTAMPTZ
);

--- Character Tables ---------

--- characters: Stores characters in the film. ---------
DROP TABLE IF EXISTS characters CASCADE;
CREATE TABLE characters (
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
    source_url VARCHAR,
    last_updated TIMESTAMPTZ
);

--- Vehicle Tables ---------

--- vehicles: Stores ships and other vehicles. ---------
DROP TABLE IF EXISTS vehicles CASCADE;
CREATE TABLE vehicles (
    id SERIAL PRIMARY KEY,
    vehicle_name VARCHAR NOT NULL,
    vehicle_type VARCHAR,
    description TEXT,
    parody_of VARCHAR,
    faction_id INTEGER REFERENCES factions (id) ON DELETE SET NULL,
    image_url VARCHAR,
    source_url VARCHAR,
    last_updated TIMESTAMPTZ
);


--- Item Tables ---------

--- items: Stores weapons, artifacts, tech, and merchandise. ---------
DROP TABLE IF EXISTS items CASCADE;
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR NOT NULL,
    item_type VARCHAR NOT NULL
        CHECK (item_type IN ('weapon', 'artifact', 'tech', 'merchandise', 'other')),
    description TEXT,
    parody_of VARCHAR,
    owner_character_id INTEGER REFERENCES characters (id) ON DELETE SET NULL,
    image_url VARCHAR,
    source_url VARCHAR,
    last_updated TIMESTAMPTZ
);

--- Quote Tables ---------

--- quotes: Stores lines of dialogue. ---------
DROP TABLE IF EXISTS quotes CASCADE;
CREATE TABLE quotes (
    id SERIAL PRIMARY KEY,
    quote_text TEXT NOT NULL,
    character_id INTEGER REFERENCES characters (id) ON DELETE SET NULL,
    source_url VARCHAR,
    last_updated TIMESTAMPTZ
);

--- Relationship Tables ---------

--- character_actors: Links a character to the actor(s) who played or voiced them. ---------
DROP TABLE IF EXISTS character_actors CASCADE;
CREATE TABLE character_actors (
    id SERIAL PRIMARY KEY,
    character_id INTEGER NOT NULL REFERENCES characters (id) ON DELETE CASCADE,
    actor_id INTEGER NOT NULL REFERENCES actors (id) ON DELETE CASCADE,
    credit_type VARCHAR
        CHECK (credit_type IN ('live_action', 'voice')),
    notes TEXT,
    UNIQUE (character_id, actor_id)
);

--- vehicle_crew: Who is aboard a vehicle, and in what role (pilot, co-pilot, captain, ...). ---------
DROP TABLE IF EXISTS vehicle_crew CASCADE;
CREATE TABLE vehicle_crew (
    vehicle_id INTEGER NOT NULL REFERENCES vehicles (id) ON DELETE CASCADE,
    character_id INTEGER NOT NULL REFERENCES characters (id) ON DELETE CASCADE,
    crew_role VARCHAR,
    PRIMARY KEY (vehicle_id, character_id)
);

--- Annotation Tables ---------
--- Both use one nullable foreign key per entity, with a CHECK that exactly one is set. ---------
--- That keeps real foreign keys (and cascades) while replacing a trivia/references ---------
--- table pair per entity with one table each. ---------

--- trivia: Stores trivia and behind-the-scenes notes for any entity. ---------
DROP TABLE IF EXISTS trivia CASCADE;
CREATE TABLE trivia (
    id SERIAL PRIMARY KEY,
    trivia_kind VARCHAR NOT NULL DEFAULT 'trivia'
        CHECK (trivia_kind IN ('trivia', 'behind_the_scenes')),
    trivia_text TEXT NOT NULL,
    character_id INTEGER REFERENCES characters (id) ON DELETE CASCADE,
    location_id INTEGER REFERENCES locations (id) ON DELETE CASCADE,
    faction_id INTEGER REFERENCES factions (id) ON DELETE CASCADE,
    vehicle_id INTEGER REFERENCES vehicles (id) ON DELETE CASCADE,
    item_id INTEGER REFERENCES items (id) ON DELETE CASCADE,
    actor_id INTEGER REFERENCES actors (id) ON DELETE CASCADE,
    CHECK (num_nonnulls(character_id, location_id, faction_id, vehicle_id,
                        item_id, actor_id) = 1)
);

--- citations: Stores numbered sources backing any entity's data. ---------
DROP TABLE IF EXISTS citations CASCADE;
CREATE TABLE citations (
    id SERIAL PRIMARY KEY,
    citation_number INTEGER NOT NULL,
    source_text TEXT NOT NULL,
    source_url VARCHAR,
    character_id INTEGER REFERENCES characters (id) ON DELETE CASCADE,
    location_id INTEGER REFERENCES locations (id) ON DELETE CASCADE,
    faction_id INTEGER REFERENCES factions (id) ON DELETE CASCADE,
    vehicle_id INTEGER REFERENCES vehicles (id) ON DELETE CASCADE,
    item_id INTEGER REFERENCES items (id) ON DELETE CASCADE,
    actor_id INTEGER REFERENCES actors (id) ON DELETE CASCADE,
    quote_id INTEGER REFERENCES quotes (id) ON DELETE CASCADE,
    CHECK (num_nonnulls(character_id, location_id, faction_id, vehicle_id,
                        item_id, actor_id, quote_id) = 1)
);
