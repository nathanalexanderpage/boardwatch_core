CREATE TABLE platform_families (
	id serial PRIMARY KEY,
	name VARCHAR (100) NULL,
	generation SMALLINT NULL,
	abbreviation VARCHAR (20) NULL,
	developer VARCHAR (100) NULL,
	name_group VARCHAR (20) NULL,
	name_prefix VARCHAR (70) NULL,
	name_suffix VARCHAR (70) NULL,
);

CREATE TABLE platform_variations (
	id serial PRIMARY KEY,
	-- here goes FK to colors_editions table --
	name VARCHAR (100) NULL,
	model_no VARCHAR (50) NULL,
	storage_capacity VARCHAR (100) NULL,
	description TEXT NULL,
	disambiguation VARCHAR (100) NULL
);

CREATE TABLE editions (
	id serial PRIMARY KEY,
	-- here goes FK to colors_editions table --
	name VARCHAR (100) NULL,
	official_color VARCHAR (60) NULL,
	note TEXT NULL,
	image_url TEXT NULL,
);

CREATE TABLE colors (
	id serial PRIMARY KEY,
	name VARCHAR (50) UNIQUE NOT NULL,
);

CREATE TABLE edition_colors (
	edition_id int NOT NULL,
	color_id int4 NOT NULL,
	PRIMARY KEY (edition_id, color_id)
);

CREATE TABLE games (
	id serial PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	year_first_release int4 NULL,
	is_bootleg boolean NOT NULL,
);

CREATE TABLE platform_game_compatibility (
	platform_id int NOT NULL,
	color_id int4 NOT NULL,
	PRIMARY KEY (edition_id, color_id)
);

CREATE TABLE platform_game_compatibility (
	platform_id int NOT NULL,
	color_id int4 NOT NULL,
	PRIMARY KEY (edition_id, color_id)
);
