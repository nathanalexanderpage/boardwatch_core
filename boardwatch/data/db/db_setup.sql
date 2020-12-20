-- requires CREATEDB permission
CREATE DATABASE boardwatch
    WITH
    ENCODING = 'UTF8';

-- requires superuser permission
SET search_path TO public;
DROP EXTENSION IF EXISTS "uuid-ossp";
CREATE EXTENSION "uuid-ossp" SCHEMA public;
DROP EXTENSION IF EXISTS pgcrypto;
CREATE EXTENSION pgcrypto SCHEMA public;
