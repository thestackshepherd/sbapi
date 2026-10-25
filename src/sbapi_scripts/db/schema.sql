/*
    This file contains the SQL schema for the Space Balls API database.
    It defines the structure of the tables and their relationships.

    Shape of the model:
    - Entities: media, episodes, actors, factions, characters, locations,
      vehicles, items, quotes. Each one is a resource the API serves.
    - Relationships: character_actors, media_characters, media_locations,
      media_vehicles, vehicle_crew. Many-to-many links between entities.
    - Annotations: trivia, citations. Shared by every entity, instead of a
      trivia/references table pair per entity.

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
  Who flies a vehicle lives in vehicle_crew, since most have more than one person aboard.
*/

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
    source_url VARCHAR,
    last_updated TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_quotes_character_id ON quotes (character_id);
CREATE INDEX IF NOT EXISTS idx_quotes_media_id ON quotes (media_id);
CREATE INDEX IF NOT EXISTS idx_quotes_episode_id ON quotes (episode_id);

/*
Relationship Table(s):
- character_actors: Links a character to the actor(s) who played or voiced them, per media entry.
- media_characters: Which characters appear in which film/show.
- media_locations: Which locations appear in which film/show.
- media_vehicles: Which vehicles appear in which film/show.
- vehicle_crew: Who is aboard a vehicle, and in what role (pilot, co-pilot, captain, ...).
*/

CREATE TABLE IF NOT EXISTS character_actors (
    id SERIAL PRIMARY KEY,
    character_id INTEGER NOT NULL REFERENCES characters (id) ON DELETE CASCADE,
    actor_id INTEGER NOT NULL REFERENCES actors (id) ON DELETE CASCADE,
    media_id INTEGER REFERENCES media (id) ON DELETE SET NULL,
    credit_type VARCHAR
        CHECK (credit_type IN ('live_action', 'voice')),
    notes TEXT,
    UNIQUE (character_id, actor_id, media_id)
);

CREATE INDEX IF NOT EXISTS idx_character_actors_character_id ON character_actors (character_id);
CREATE INDEX IF NOT EXISTS idx_character_actors_actor_id ON character_actors (actor_id);
CREATE INDEX IF NOT EXISTS idx_character_actors_media_id ON character_actors (media_id);

CREATE TABLE IF NOT EXISTS media_characters (
    media_id INTEGER NOT NULL REFERENCES media (id) ON DELETE CASCADE,
    character_id INTEGER NOT NULL REFERENCES characters (id) ON DELETE CASCADE,
    PRIMARY KEY (media_id, character_id)
);

CREATE INDEX IF NOT EXISTS idx_media_characters_character_id ON media_characters (character_id);

CREATE TABLE IF NOT EXISTS media_locations (
    media_id INTEGER NOT NULL REFERENCES media (id) ON DELETE CASCADE,
    location_id INTEGER NOT NULL REFERENCES locations (id) ON DELETE CASCADE,
    PRIMARY KEY (media_id, location_id)
);

CREATE INDEX IF NOT EXISTS idx_media_locations_location_id ON media_locations (location_id);

CREATE TABLE IF NOT EXISTS media_vehicles (
    media_id INTEGER NOT NULL REFERENCES media (id) ON DELETE CASCADE,
    vehicle_id INTEGER NOT NULL REFERENCES vehicles (id) ON DELETE CASCADE,
    PRIMARY KEY (media_id, vehicle_id)
);

CREATE INDEX IF NOT EXISTS idx_media_vehicles_vehicle_id ON media_vehicles (vehicle_id);

CREATE TABLE IF NOT EXISTS vehicle_crew (
    vehicle_id INTEGER NOT NULL REFERENCES vehicles (id) ON DELETE CASCADE,
    character_id INTEGER NOT NULL REFERENCES characters (id) ON DELETE CASCADE,
    crew_role VARCHAR,
    PRIMARY KEY (vehicle_id, character_id)
);

CREATE INDEX IF NOT EXISTS idx_vehicle_crew_character_id ON vehicle_crew (character_id);

/*
Annotation Table(s):
- trivia: Trivia and behind-the-scenes notes for any entity.
- citations: Numbered sources backing any entity's data.
  Both use one nullable foreign key per entity, with a CHECK that exactly one is set.
  That keeps real foreign keys (and cascades) while replacing a trivia/references
  table pair per entity with one table each.
*/

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
    media_id INTEGER REFERENCES media (id) ON DELETE CASCADE,
    episode_id INTEGER REFERENCES episodes (id) ON DELETE CASCADE,
    actor_id INTEGER REFERENCES actors (id) ON DELETE CASCADE,
    CHECK (num_nonnulls(character_id, location_id, faction_id, vehicle_id,
                        item_id, media_id, episode_id, actor_id) = 1)
);

CREATE INDEX IF NOT EXISTS idx_trivia_character_id ON trivia (character_id);
CREATE INDEX IF NOT EXISTS idx_trivia_location_id ON trivia (location_id);
CREATE INDEX IF NOT EXISTS idx_trivia_faction_id ON trivia (faction_id);
CREATE INDEX IF NOT EXISTS idx_trivia_vehicle_id ON trivia (vehicle_id);
CREATE INDEX IF NOT EXISTS idx_trivia_item_id ON trivia (item_id);
CREATE INDEX IF NOT EXISTS idx_trivia_media_id ON trivia (media_id);
CREATE INDEX IF NOT EXISTS idx_trivia_episode_id ON trivia (episode_id);
CREATE INDEX IF NOT EXISTS idx_trivia_actor_id ON trivia (actor_id);

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
    media_id INTEGER REFERENCES media (id) ON DELETE CASCADE,
    episode_id INTEGER REFERENCES episodes (id) ON DELETE CASCADE,
    actor_id INTEGER REFERENCES actors (id) ON DELETE CASCADE,
    quote_id INTEGER REFERENCES quotes (id) ON DELETE CASCADE,
    CHECK (num_nonnulls(character_id, location_id, faction_id, vehicle_id,
                        item_id, media_id, episode_id, actor_id, quote_id) = 1)
);

CREATE INDEX IF NOT EXISTS idx_citations_character_id ON citations (character_id);
CREATE INDEX IF NOT EXISTS idx_citations_location_id ON citations (location_id);
CREATE INDEX IF NOT EXISTS idx_citations_faction_id ON citations (faction_id);
CREATE INDEX IF NOT EXISTS idx_citations_vehicle_id ON citations (vehicle_id);
CREATE INDEX IF NOT EXISTS idx_citations_item_id ON citations (item_id);
CREATE INDEX IF NOT EXISTS idx_citations_media_id ON citations (media_id);
CREATE INDEX IF NOT EXISTS idx_citations_episode_id ON citations (episode_id);
CREATE INDEX IF NOT EXISTS idx_citations_actor_id ON citations (actor_id);
CREATE INDEX IF NOT EXISTS idx_citations_quote_id ON citations (quote_id);
