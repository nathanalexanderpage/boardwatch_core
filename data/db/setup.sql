CREATE TABLE platform_families (
	id serial PRIMARY KEY,
	name varchar(100) NULL,
	abbreviation varchar(20) NULL,
	developer varchar(100) NULL,
);

CREATE TABLE platform_name_groups (
	id serial PRIMARY KEY,
	name varchar(50) NULL,
	abbr varchar(30) NULL
);

CREATE TABLE platforms (
	id serial PRIMARY KEY,
	name varchar(100) NULL,
	platform_family smallint NULL, --FK
	name_group smallint NULL, --FK
	model_no varchar(50) NULL,
	storage_capacity varchar(100) NULL,
	description text NULL,
	disambiguation varchar(100) NULL,
	relevance smallint NULL --#/10
);

CREATE TABLE platform_editions (
	id serial PRIMARY KEY,
	name varchar(100) NULL,
	official_color varchar(60) NULL,
	has_matte boolean NULL,
	has_transparency boolean NULL,
	has_gloss boolean NULL,
	note text NULL,
	image_url text NULL
);

CREATE TABLE colors (
	id serial PRIMARY KEY,
	name varchar(50) UNIQUE NOT NULL
);

CREATE TABLE platform_editions_colors (
	platform_edition_id int NOT NULL, --FK
	color_id smallint NOT NULL, --FK
	PRIMARY KEY (platform_edition_id, color_id)
);

CREATE TABLE games (
	id serial PRIMARY KEY,
	name varchar(255) NOT NULL,
	year_first_release smallint NULL,
	is_bootleg boolean NOT NULL
);

CREATE TABLE platforms_games_compatibility (
	platform_id int NOT NULL,
	game_id int NOT NULL,
	PRIMARY KEY (platform_id, game_id)
);

CREATE TABLE accessory_types (
	id serial PRIMARY KEY,
	name varchar(100) NOT NULL,
	description varchar(255) NULL,
);

CREATE TABLE accessories (
	id serial PRIMARY KEY,
	name varchar(255) NOT NULL,
	type smallint NOT NULL, --FK
	year_first_release smallint NULL,
	is_first_party boolean NOT NULL,
	description text
);

CREATE TABLE games_accessories_compatibility (
	game_id int NOT NULL,
	accessory_id int NOT NULL,
	PRIMARY KEY (game_id, accessory_id)
);

CREATE TABLE platforms_accessories_compatibility (
	platform_id int NOT NULL,
	accessory_id int NOT NULL,
	PRIMARY KEY (platform_id, accessory_id)
);

CREATE TABLE accessory_variations (
	accessory_id int NOT NULL, --FK
	description varchar(255) NOT NULL
);

CREATE TABLE accessory_variations_colors (
	accessory_variation_id int NOT NULL, --FK
	color_id int NOT NULL --FK
);

CREATE TABLE characters (
	id serial PRIMARY KEY,
	name varchar(150) NOT NULL,
	name_disambiguation varchar(150) NULL,
	from_what varchar(255) NOT NULL,
);

CREATE TABLE characters_in_games (
	character_id int NOT NULL,
	game_id int NOT NULL,
	PRIMARY KEY (character_id, game_id),
	is_playable boolean NOT NULL,
	playability_extent text NULL
);
