--- Space Balls API database schema ---------

--- actors: Stores real-world cast members. ---------
DROP TABLE IF EXISTS actors CASCADE;
CREATE TABLE actors (
    id            SERIAL  PRIMARY KEY,
    actor_name    VARCHAR UNIQUE NOT NULL,
    last_updated  TIMESTAMPTZ
);
CREATE INDEX CONCURRENTLY idx_actors ON actors (actor_name);


--- locations: Stores planets, moons, and other settings. ---------
DROP TABLE IF EXISTS planets CASCADE;
CREATE TABLE planets(
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    ruler_id VARCHAR,
    planet_type VARCHAR,
    description TEXT,
    government VARCHAR,
    capital VARCHAR,
    parody_of VARCHAR,
    last_updated TIMESTAMPTZ
);

CREATE INDEX CONCURRENTLY idx_planets ON planets(name);

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

CREATE INDEX CONCURRENTLY idx_characters_name ON characters (character_name);
CREATE INDEX CONCURRENTLY idx_characters_faction_id ON characters (faction_id);
CREATE INDEX CONCURRENTLY idx_characters_homeworld_id ON characters (homeworld_id);

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

CREATE INDEX CONCURRENTLY idx_vehicles_name ON vehicles (vehicle_name);
CREATE INDEX CONCURRENTLY idx_vehicles_faction_id ON vehicles (faction_id);

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

CREATE INDEX CONCURRENTLY idx_items_name ON items (item_name);
CREATE INDEX CONCURRENTLY idx_items_owner_character_id ON items (owner_character_id);

--- quotes: Stores lines of dialogue. ---------
DROP TABLE IF EXISTS quotes CASCADE;
CREATE TABLE quotes (
    id SERIAL PRIMARY KEY,
    quote_text TEXT NOT NULL,
    character_id INTEGER REFERENCES characters (id) ON DELETE SET NULL,
    source_url VARCHAR,
    last_updated TIMESTAMPTZ
);

CREATE INDEX CONCURRENTLY idx_quotes_character_id ON quotes (character_id);

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

CREATE INDEX CONCURRENTLY idx_character_actors_actor_id ON character_actors (actor_id);

--- vehicle_crew: Who is aboard a vehicle, and in what role (pilot, co-pilot, captain, ...). ---------
DROP TABLE IF EXISTS vehicle_crew CASCADE;
CREATE TABLE vehicle_crew (
    vehicle_id INTEGER NOT NULL REFERENCES vehicles (id) ON DELETE CASCADE,
    character_id INTEGER NOT NULL REFERENCES characters (id) ON DELETE CASCADE,
    crew_role VARCHAR,
    PRIMARY KEY (vehicle_id, character_id)
);

CREATE INDEX CONCURRENTLY idx_vehicle_crew_character_id ON vehicle_crew (character_id);

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

CREATE INDEX CONCURRENTLY idx_trivia_character_id ON trivia (character_id);
CREATE INDEX CONCURRENTLY idx_trivia_location_id ON trivia (location_id);
CREATE INDEX CONCURRENTLY idx_trivia_faction_id ON trivia (faction_id);
CREATE INDEX CONCURRENTLY idx_trivia_vehicle_id ON trivia (vehicle_id);
CREATE INDEX CONCURRENTLY idx_trivia_item_id ON trivia (item_id);
CREATE INDEX CONCURRENTLY idx_trivia_actor_id ON trivia (actor_id);

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

CREATE INDEX CONCURRENTLY idx_citations_character_id ON citations (character_id);
CREATE INDEX CONCURRENTLY idx_citations_location_id ON citations (location_id);
CREATE INDEX CONCURRENTLY idx_citations_faction_id ON citations (faction_id);
CREATE INDEX CONCURRENTLY idx_citations_vehicle_id ON citations (vehicle_id);
CREATE INDEX CONCURRENTLY idx_citations_item_id ON citations (item_id);
CREATE INDEX CONCURRENTLY idx_citations_actor_id ON citations (actor_id);
CREATE INDEX CONCURRENTLY idx_citations_quote_id ON citations (quote_id);
