CREATE DATABASE boardwatch
    WITH
    ENCODING = 'UTF8';

CREATE TABLE platform_families (
	id serial PRIMARY KEY,
	name varchar(100) NULL,
	generation smallint NULL,
	developer varchar(100) NULL
);

CREATE TABLE platform_name_groups (
	id serial PRIMARY KEY,
	name varchar(50) NULL,
	description varchar(100) NULL
);

CREATE TABLE platforms (
	id serial PRIMARY KEY,
	name varchar(100) NULL,
	platform_family_id smallint NULL REFERENCES platform_families(id),
	name_group_id smallint NULL REFERENCES platform_name_groups(id),
	is_brand_missing boolean NOT NULL,
	model_no varchar(50) NULL,
	storage_capacity varchar(100) NULL,
	description text NULL,
	disambiguation varchar(100) NULL,
	relevance smallint NULL -- (#/10)
);

CREATE TABLE colors (
	id serial PRIMARY KEY,
	name varchar(50) UNIQUE NOT NULL
);

CREATE TABLE platform_editions (
	id serial PRIMARY KEY,
	name varchar(100) NULL,
	platform_id smallint NULL REFERENCES platforms(id),
	official_color varchar(60) NULL,
	has_matte boolean NULL,
	has_transparency boolean NULL,
	has_gloss boolean NULL,
	note text NULL,
	image_url text NULL
);

CREATE TABLE colors_platform_editions (
	platform_edition_id int NOT NULL REFERENCES platform_editions(id),
	color_id smallint NOT NULL REFERENCES colors(id),
	PRIMARY KEY (platform_edition_id, color_id)
);

CREATE TABLE games (
	id serial PRIMARY KEY,
	name varchar(255) NOT NULL,
	year_first_release smallint NULL,
	is_bootleg boolean NOT NULL
);

CREATE TABLE games_platforms_compatibility (
	platform_id int NOT NULL REFERENCES platforms(id),
	game_id int NOT NULL REFERENCES games(id),
	PRIMARY KEY (platform_id, game_id)
);

CREATE TABLE accessory_types (
	id serial PRIMARY KEY,
	name varchar(100) NOT NULL,
	description varchar(255) NULL
);

CREATE TABLE accessories (
	id serial PRIMARY KEY,
	name varchar(255) NOT NULL,
	type smallint NOT NULL REFERENCES accessory_types(id),
	year_first_release smallint NULL,
	is_first_party boolean NOT NULL,
	description text
);

CREATE TABLE accessories_games_compatibility (
	game_id int NOT NULL REFERENCES games(id),
	accessory_id int NOT NULL REFERENCES accessories(id),
	PRIMARY KEY (game_id, accessory_id)
);

CREATE TABLE accessories_platforms_compatibility (
	platform_id int NOT NULL REFERENCES platforms(id),
	accessory_id int NOT NULL REFERENCES accessories(id),
	PRIMARY KEY (platform_id, accessory_id)
);

CREATE TABLE accessory_variations (
	id serial PRIMARY KEY,
	accessory_id int NOT NULL REFERENCES accessories(id),
	description varchar(255) NOT NULL
);

CREATE TABLE accessory_variations_colors (
	accessory_variation_id int NOT NULL REFERENCES accessory_variations(id),
	color_id int NOT NULL REFERENCES colors(id)
);

CREATE TABLE characters (
	id serial PRIMARY KEY,
	name varchar(150) NOT NULL,
	name_disambiguation varchar(150) NULL,
	from_what varchar(255) NOT NULL
);

CREATE TABLE characters_in_games (
	character_id int NOT NULL REFERENCES characters(id),
	game_id int NOT NULL REFERENCES games(id),
	PRIMARY KEY (character_id, game_id),
	is_playable boolean NOT NULL,
	playability_extent text NULL
);
