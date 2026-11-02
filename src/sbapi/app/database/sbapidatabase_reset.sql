--- Space Balls API database reset ---------

--- Drops EVERY table (and anything else) in the public schema, then recreates it empty. ---------
--- Run this before sbapidatabase_schema.sql to start over from only what the schema defines. ---------
--- psql -f sbapidatabase_reset.sql -f sbapidatabase_schema.sql ---------

DROP SCHEMA IF EXISTS public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO PUBLIC;
