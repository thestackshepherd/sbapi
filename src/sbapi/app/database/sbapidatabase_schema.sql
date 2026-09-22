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
