# SBAPI Entity Relationship Diagram

Auto-generated from `sbapidatabase_schema.sql` by `scripts/generate_erd.py`. Do not edit by hand — rerun the script after changing the schema.

## Overview

Full relationship graph, no columns (see the per-domain diagrams below for detail).

```mermaid
%%{init: {'er': {'useMaxWidth': false}, 'themeVariables': {'fontSize': '18px'}}}%%
erDiagram
    media ||--|{ episodes : "media_id"
    characters ||--o{ factions : "leader_id"
    characters ||--o{ locations : "ruler_id"
    characters ||--o{ locations : "heir_id"
    factions ||--o{ characters : "faction_id"
    locations ||--o{ characters : "homeworld_id"
    factions ||--o{ vehicles : "faction_id"
    characters ||--o{ items : "owner_character_id"
    characters ||--o{ quotes : "character_id"
    media ||--o{ quotes : "media_id"
    episodes ||--o{ quotes : "episode_id"
    characters ||--|{ character_actors : "character_id"
    actors ||--|{ character_actors : "actor_id"
    media ||--o{ character_actors : "media_id"
    media ||--|{ media_characters : "media_id"
    characters ||--|{ media_characters : "character_id"
    media ||--|{ media_locations : "media_id"
    locations ||--|{ media_locations : "location_id"
    media ||--|{ media_vehicles : "media_id"
    vehicles ||--|{ media_vehicles : "vehicle_id"
    vehicles ||--|{ vehicle_crew : "vehicle_id"
    characters ||--|{ vehicle_crew : "character_id"
    characters ||--o{ trivia : "character_id"
    locations ||--o{ trivia : "location_id"
    factions ||--o{ trivia : "faction_id"
    vehicles ||--o{ trivia : "vehicle_id"
    items ||--o{ trivia : "item_id"
    media ||--o{ trivia : "media_id"
    episodes ||--o{ trivia : "episode_id"
    actors ||--o{ trivia : "actor_id"
    characters ||--o{ citations : "character_id"
    locations ||--o{ citations : "location_id"
    factions ||--o{ citations : "faction_id"
    vehicles ||--o{ citations : "vehicle_id"
    items ||--o{ citations : "item_id"
    media ||--o{ citations : "media_id"
    episodes ||--o{ citations : "episode_id"
    actors ||--o{ citations : "actor_id"
    quotes ||--o{ citations : "quote_id"
```

## Relationships

```mermaid
%%{init: {'er': {'useMaxWidth': false}, 'themeVariables': {'fontSize': '18px'}}}%%
erDiagram
    character_actors {
        int id PK
        int character_id FK
        int actor_id FK
        int media_id FK
        string credit_type
        string notes
    }
    media_characters {
        int media_id PK,FK
        int character_id PK,FK
    }
    media_locations {
        int media_id PK,FK
        int location_id PK,FK
    }
    media_vehicles {
        int media_id PK,FK
        int vehicle_id PK,FK
    }
    vehicle_crew {
        int vehicle_id PK,FK
        int character_id PK,FK
        string crew_role
    }
    characters ||--|{ character_actors : "character_id"
    actors ||--|{ character_actors : "actor_id"
    media ||--o{ character_actors : "media_id"
    media ||--|{ media_characters : "media_id"
    characters ||--|{ media_characters : "character_id"
    media ||--|{ media_locations : "media_id"
    locations ||--|{ media_locations : "location_id"
    media ||--|{ media_vehicles : "media_id"
    vehicles ||--|{ media_vehicles : "vehicle_id"
    vehicles ||--|{ vehicle_crew : "vehicle_id"
    characters ||--|{ vehicle_crew : "character_id"
```

## Annotations

```mermaid
%%{init: {'er': {'useMaxWidth': false}, 'themeVariables': {'fontSize': '18px'}}}%%
erDiagram
    citations {
        int id PK
        int citation_number
        string source_text
        string source_url
        int character_id FK
        int location_id FK
        int faction_id FK
        int vehicle_id FK
        int item_id FK
        int media_id FK
        int episode_id FK
        int actor_id FK
        int quote_id FK
    }
    trivia {
        int id PK
        string trivia_kind
        string trivia_text
        int character_id FK
        int location_id FK
        int faction_id FK
        int vehicle_id FK
        int item_id FK
        int media_id FK
        int episode_id FK
        int actor_id FK
    }
    characters ||--o{ trivia : "character_id"
    locations ||--o{ trivia : "location_id"
    factions ||--o{ trivia : "faction_id"
    vehicles ||--o{ trivia : "vehicle_id"
    items ||--o{ trivia : "item_id"
    media ||--o{ trivia : "media_id"
    episodes ||--o{ trivia : "episode_id"
    actors ||--o{ trivia : "actor_id"
    characters ||--o{ citations : "character_id"
    locations ||--o{ citations : "location_id"
    factions ||--o{ citations : "faction_id"
    vehicles ||--o{ citations : "vehicle_id"
    items ||--o{ citations : "item_id"
    media ||--o{ citations : "media_id"
    episodes ||--o{ citations : "episode_id"
    actors ||--o{ citations : "actor_id"
    quotes ||--o{ citations : "quote_id"
```

## Media

```mermaid
%%{init: {'er': {'useMaxWidth': false}, 'themeVariables': {'fontSize': '18px'}}}%%
erDiagram
    episodes {
        int id PK
        int media_id FK
        int season_number
        int episode_number
        string title
        string description
        date air_date
        string source_url
        timestamp last_updated
    }
    media {
        int id PK
        string title
        string media_type
        date release_date
        string description
        string image_url
        string source_url
        timestamp last_updated
    }
    media ||--|{ episodes : "media_id"
```

## People

```mermaid
%%{init: {'er': {'useMaxWidth': false}, 'themeVariables': {'fontSize': '18px'}}}%%
erDiagram
    actors {
        int id PK
        string actor_name
        string image_url
        string source_url
        timestamp last_updated
    }
    characters {
        int id PK
        string character_name
        string full_name
        string species
        string gender
        string character_role
        string parody_of
        int faction_id FK
        int homeworld_id FK
        string image_url
        string source_url
        timestamp last_updated
    }
    factions {
        int id PK
        string faction_name
        string description
        string parody_of
        string image_url
        string source_url
        timestamp last_updated
        int leader_id FK
    }
    characters ||--o{ factions : "leader_id"
    factions ||--o{ characters : "faction_id"
    locations ||--o{ characters : "homeworld_id"
```

## Things

```mermaid
%%{init: {'er': {'useMaxWidth': false}, 'themeVariables': {'fontSize': '18px'}}}%%
erDiagram
    items {
        int id PK
        string item_name
        string item_type
        string description
        string parody_of
        int owner_character_id FK
        string image_url
        string source_url
        timestamp last_updated
    }
    locations {
        int id PK
        string name
        string location_type
        string description
        string parody_of
        string image_url
        string source_url
        timestamp last_updated
        int ruler_id FK
        int heir_id FK
    }
    quotes {
        int id PK
        string quote_text
        int character_id FK
        int media_id FK
        int episode_id FK
        string source_url
        timestamp last_updated
    }
    vehicles {
        int id PK
        string vehicle_name
        string vehicle_type
        string description
        string parody_of
        int faction_id FK
        string image_url
        string source_url
        timestamp last_updated
    }
    characters ||--o{ locations : "ruler_id"
    characters ||--o{ locations : "heir_id"
    factions ||--o{ vehicles : "faction_id"
    characters ||--o{ items : "owner_character_id"
    characters ||--o{ quotes : "character_id"
    media ||--o{ quotes : "media_id"
    episodes ||--o{ quotes : "episode_id"
```

## Tables

### actors

| Column | Type | Key |
|---|---|---|
| id | SERIAL | PK |
| actor_name | VARCHAR |  |
| image_url | VARCHAR |  |
| source_url | VARCHAR |  |
| last_updated | TIMESTAMPTZ |  |

### character_actors

| Column | Type | Key |
|---|---|---|
| id | SERIAL | PK |
| character_id | INTEGER | FK → characters |
| actor_id | INTEGER | FK → actors |
| media_id | INTEGER | FK → media |
| credit_type | VARCHAR |  |
| notes | TEXT |  |

### characters

| Column | Type | Key |
|---|---|---|
| id | SERIAL | PK |
| character_name | VARCHAR |  |
| full_name | VARCHAR |  |
| species | VARCHAR |  |
| gender | VARCHAR |  |
| character_role | VARCHAR |  |
| parody_of | VARCHAR |  |
| faction_id | INTEGER | FK → factions |
| homeworld_id | INTEGER | FK → locations |
| image_url | VARCHAR |  |
| source_url | VARCHAR |  |
| last_updated | TIMESTAMPTZ |  |

### citations

| Column | Type | Key |
|---|---|---|
| id | SERIAL | PK |
| citation_number | INTEGER |  |
| source_text | TEXT |  |
| source_url | VARCHAR |  |
| character_id | INTEGER | FK → characters |
| location_id | INTEGER | FK → locations |
| faction_id | INTEGER | FK → factions |
| vehicle_id | INTEGER | FK → vehicles |
| item_id | INTEGER | FK → items |
| media_id | INTEGER | FK → media |
| episode_id | INTEGER | FK → episodes |
| actor_id | INTEGER | FK → actors |
| quote_id | INTEGER | FK → quotes |

### episodes

| Column | Type | Key |
|---|---|---|
| id | SERIAL | PK |
| media_id | INTEGER | FK → media |
| season_number | INTEGER |  |
| episode_number | INTEGER |  |
| title | VARCHAR |  |
| description | TEXT |  |
| air_date | DATE |  |
| source_url | VARCHAR |  |
| last_updated | TIMESTAMPTZ |  |

### factions

| Column | Type | Key |
|---|---|---|
| id | SERIAL | PK |
| faction_name | VARCHAR |  |
| description | TEXT |  |
| parody_of | VARCHAR |  |
| image_url | VARCHAR |  |
| source_url | VARCHAR |  |
| last_updated | TIMESTAMPTZ |  |
| leader_id | INTEGER | FK → characters |

### items

| Column | Type | Key |
|---|---|---|
| id | SERIAL | PK |
| item_name | VARCHAR |  |
| item_type | VARCHAR |  |
| description | TEXT |  |
| parody_of | VARCHAR |  |
| owner_character_id | INTEGER | FK → characters |
| image_url | VARCHAR |  |
| source_url | VARCHAR |  |
| last_updated | TIMESTAMPTZ |  |

### locations

| Column | Type | Key |
|---|---|---|
| id | SERIAL | PK |
| name | VARCHAR |  |
| location_type | VARCHAR |  |
| description | TEXT |  |
| parody_of | VARCHAR |  |
| image_url | VARCHAR |  |
| source_url | VARCHAR |  |
| last_updated | TIMESTAMPTZ |  |
| ruler_id | INTEGER | FK → characters |
| heir_id | INTEGER | FK → characters |

### media

| Column | Type | Key |
|---|---|---|
| id | SERIAL | PK |
| title | VARCHAR |  |
| media_type | VARCHAR |  |
| release_date | DATE |  |
| description | TEXT |  |
| image_url | VARCHAR |  |
| source_url | VARCHAR |  |
| last_updated | TIMESTAMPTZ |  |

### media_characters

| Column | Type | Key |
|---|---|---|
| media_id | INTEGER | PK, FK → media |
| character_id | INTEGER | PK, FK → characters |

### media_locations

| Column | Type | Key |
|---|---|---|
| media_id | INTEGER | PK, FK → media |
| location_id | INTEGER | PK, FK → locations |

### media_vehicles

| Column | Type | Key |
|---|---|---|
| media_id | INTEGER | PK, FK → media |
| vehicle_id | INTEGER | PK, FK → vehicles |

### quotes

| Column | Type | Key |
|---|---|---|
| id | SERIAL | PK |
| quote_text | TEXT |  |
| character_id | INTEGER | FK → characters |
| media_id | INTEGER | FK → media |
| episode_id | INTEGER | FK → episodes |
| source_url | VARCHAR |  |
| last_updated | TIMESTAMPTZ |  |

### trivia

| Column | Type | Key |
|---|---|---|
| id | SERIAL | PK |
| trivia_kind | VARCHAR |  |
| trivia_text | TEXT |  |
| character_id | INTEGER | FK → characters |
| location_id | INTEGER | FK → locations |
| faction_id | INTEGER | FK → factions |
| vehicle_id | INTEGER | FK → vehicles |
| item_id | INTEGER | FK → items |
| media_id | INTEGER | FK → media |
| episode_id | INTEGER | FK → episodes |
| actor_id | INTEGER | FK → actors |

### vehicle_crew

| Column | Type | Key |
|---|---|---|
| vehicle_id | INTEGER | PK, FK → vehicles |
| character_id | INTEGER | PK, FK → characters |
| crew_role | VARCHAR |  |

### vehicles

| Column | Type | Key |
|---|---|---|
| id | SERIAL | PK |
| vehicle_name | VARCHAR |  |
| vehicle_type | VARCHAR |  |
| description | TEXT |  |
| parody_of | VARCHAR |  |
| faction_id | INTEGER | FK → factions |
| image_url | VARCHAR |  |
| source_url | VARCHAR |  |
| last_updated | TIMESTAMPTZ |  |
