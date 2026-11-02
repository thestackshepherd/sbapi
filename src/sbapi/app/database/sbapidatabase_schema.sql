--- Space Balls API database schema ---------

--- Actor Tables ---------

--- actors: Stores real-world cast members. ---------
CREATE TABLE IF NOT EXISTS actors (
    id            SERIAL  PRIMARY KEY,
    actor_name    VARCHAR NOT NULL,
    image_url     VARCHAR,
    source_url    VARCHAR,
    last_updated  TIMESTAMPTZ
);

--- Faction Tables ---------

--- factions: Stores the groups characters and vehicles belong to. ---------
CREATE TABLE IF NOT EXISTS factions (
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
CREATE TABLE IF NOT EXISTS locations (
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
    source_url VARCHAR,
    last_updated TIMESTAMPTZ
);

--- Vehicle Tables ---------

--- vehicles: Stores ships and other vehicles. ---------
CREATE TABLE IF NOT EXISTS vehicles (
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

CREATE INDEX IF NOT EXISTS idx_vehicles_faction_id ON vehicles (faction_id);

--- Item Tables ---------

--- items: Stores weapons, artifacts, tech, and merchandise. ---------
CREATE TABLE IF NOT EXISTS items (
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

CREATE INDEX IF NOT EXISTS idx_items_owner_character_id ON items (owner_character_id);

--- Quote Tables ---------

--- quotes: Stores lines of dialogue. ---------
CREATE TABLE IF NOT EXISTS quotes (
    id SERIAL PRIMARY KEY,
    quote_text TEXT NOT NULL,
    character_id INTEGER REFERENCES characters (id) ON DELETE SET NULL,
    source_url VARCHAR,
    last_updated TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_quotes_character_id ON quotes (character_id);

--- Relationship Tables ---------

--- character_actors: Links a character to the actor(s) who played or voiced them. ---------
CREATE TABLE IF NOT EXISTS character_actors (
    id SERIAL PRIMARY KEY,
    character_id INTEGER NOT NULL REFERENCES characters (id) ON DELETE CASCADE,
    actor_id INTEGER NOT NULL REFERENCES actors (id) ON DELETE CASCADE,
    credit_type VARCHAR
        CHECK (credit_type IN ('live_action', 'voice')),
    notes TEXT,
    UNIQUE (character_id, actor_id)
);

--- vehicle_crew: Who is aboard a vehicle, and in what role (pilot, co-pilot, captain, ...). ---------
CREATE TABLE IF NOT EXISTS vehicle_crew (
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
CREATE TABLE IF NOT EXISTS trivia (
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
CREATE TABLE IF NOT EXISTS citations (
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
