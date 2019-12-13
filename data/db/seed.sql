INSERT INTO platform_families (name, generation, abbreviation, developer) VALUES('Nintendo Entertainment System', 3, 'NES', 'Nintendo');
-- INSERT INTO platform_families (name, generation, abbreviation, developer) VALUES('Family Computer', 3, 'famicom', 'Nintendo');
-- INSERT INTO platform_families (name, generation, abbreviation, developer) VALUES('Family Computer Disk System', 3, 'fds', 'Nintendo');
INSERT INTO platform_families (name, generation, abbreviation, developer) VALUES('Super Nintendo Entertainment System', 4, 'SNES', 'Nintendo');
-- INSERT INTO platform_families (name, generation, abbreviation, developer) VALUES('Super Famicom', 4, 'SFC', 'Nintendo');
INSERT INTO platform_families (name, generation, abbreviation, developer) VALUES('Game Boy', 4, 'GB', 'Nintendo');
INSERT INTO platform_families (name, generation, abbreviation, developer) VALUES('Nintendo 64', 5, 'N64', 'Nintendo');
INSERT INTO platform_families (name, generation, abbreviation, developer) VALUES('Virtual Boy', 5, NULL, 'Nintendo');
INSERT INTO platform_families (name, generation, abbreviation, developer) VALUES('GameCube', 6, 'GCN', 'Nintendo');
INSERT INTO platform_families (name, generation, abbreviation, developer) VALUES('Game Boy Advance', 6, 'GBA', 'Nintendo');
INSERT INTO platform_families (name, generation, abbreviation, developer) VALUES('Wii', 7, 'Wii', 'Nintendo');
INSERT INTO platform_families (name, generation, abbreviation, developer) VALUES('DS', 7, NULL, 'Nintendo');
INSERT INTO platform_families (name, generation, abbreviation, developer) VALUES('Nintendo DSi', 7, NULL, 'Nintendo');
INSERT INTO platform_families (name, generation, abbreviation, developer) VALUES('Wii U', 8, NULL, 'Nintendo');
INSERT INTO platform_families (name, generation, abbreviation, developer) VALUES('New Nintendo 3DS', 8, NULL, 'Nintendo');
INSERT INTO platform_families (name, generation, abbreviation, developer) VALUES('3DS', 8, NULL, 'Nintendo');
INSERT INTO platform_families (name, generation, abbreviation, developer) VALUES('Switch', 8, NULL, 'Nintendo');
INSERT INTO platform_families (name, generation, abbreviation, developer) VALUES('SG-1000', 3, NULL, 'Sega');
INSERT INTO platform_families (name, generation, abbreviation, developer) VALUES('Sega Game Gear', 4, 'Game Gear', 'Sega');
INSERT INTO platform_families (name, generation, abbreviation, developer) VALUES('Sega 32X', 4, 'Sega32', 'Sega');
INSERT INTO platform_families (name, generation, abbreviation, developer) VALUES('Sega CD', 4, NULL, 'Sega');
INSERT INTO platform_families (name, generation, abbreviation, developer) VALUES('Genesis', 4, NULL, 'Sega');
INSERT INTO platform_families (name, generation, abbreviation, developer) VALUES('Saturn', 5, NULL, 'Sega');
INSERT INTO platform_families (name, generation, abbreviation, developer) VALUES('Sega Master System', 3, 'SMS', 'Sega');
INSERT INTO platform_families (name, generation, abbreviation, developer) VALUES('Xbox', 6, NULL, 'Microsoft');
INSERT INTO platform_families (name, generation, abbreviation, developer) VALUES('Xbox 360', 7, NULL, 'Microsoft');
INSERT INTO platform_families (name, generation, abbreviation, developer) VALUES('Xbox One', 8, NULL, 'Microsoft');
INSERT INTO platform_families (name, generation, abbreviation, developer) VALUES('Xbox Project Scarlett', NULL, NULL, 'Sega');
INSERT INTO platform_families (name, generation, abbreviation, developer) VALUES('PlayStation 2', 6, 'PS2', 'Sony');
INSERT INTO platform_families (name, generation, abbreviation, developer) VALUES('PlayStation 3', 7, 'PS3', 'Sony');
INSERT INTO platform_families (name, generation, abbreviation, developer) VALUES('PlayStation Portable', 7, 'PSP', 'Sony');
INSERT INTO platform_families (name, generation, abbreviation, developer) VALUES('PlayStation 4', 8, 'PS4', 'Sony');
INSERT INTO platform_families (name, generation, abbreviation, developer) VALUES('PlayStation Vita', 8, 'Vita', 'Sony');
INSERT INTO platform_families (name, generation, abbreviation, developer) VALUES('PlayStation 5', NULL, 'PS5', 'Sony');

INSERT INTO platform_name_groups (name, description) VALUES('Nintendo Entertainment System', 'started by the Nintendo Entertainment System (NES)');
INSERT INTO platform_name_groups (name, description) VALUES('Game Boy', 'started by the Game Boy');
INSERT INTO platform_name_groups (name, description) VALUES('Wii', 'started by the Wii');
INSERT INTO platform_name_groups (name, description) VALUES('DS', 'started by the Nintendo DS');
INSERT INTO platform_name_groups (name, description) VALUES('PlayStation', 'started by the original PlayStation');
INSERT INTO platform_name_groups (name, description) VALUES('Xbox', 'started by the original Xbox');

-- INSERT INTO table (column, column, column, column, column, column, column) VALUES('pink', 'pink', 'pink', 'pink', 'pink', 'pink', 'pink');

-- INSERT INTO platforms (name, platform_family, name_group, model_no, storage_capacity, description, disambiguation, estimated_relevance) VALUES('GameCube', 'FK', 'FK', 'DOL-001', 'pink', 'Nintendo''s ______th home console, debuted in', 'the original GameCube', 10);

-- INSERT INTO platform_editions (name, official_color, note, image_url_filename) VALUES(NULL, 'Indigo', NULL, NULL);

INSERT INTO colors (name) VALUES('pink');
INSERT INTO colors (name) VALUES('red');
INSERT INTO colors (name) VALUES('orange');
INSERT INTO colors (name) VALUES('yellow');
INSERT INTO colors (name) VALUES('green');
INSERT INTO colors (name) VALUES('mint');
INSERT INTO colors (name) VALUES('blue');
INSERT INTO colors (name) VALUES('navy');
INSERT INTO colors (name) VALUES('purple');
INSERT INTO colors (name) VALUES('black');
INSERT INTO colors (name) VALUES('white');
INSERT INTO colors (name) VALUES('off-white');
INSERT INTO colors (name) VALUES('brown');
INSERT INTO colors (name) VALUES('grey');
INSERT INTO colors (name) VALUES('gold');
INSERT INTO colors (name) VALUES('silver');

-- INSERT INTO platform_editions_colors (platform_edition_id, color_id, has_matte, has_transparency, has_gloss) VALUES(1, 1, false, false, false);

-- INSERT INTO games (name, year_first_release, is_bootleg) VALUES('Super Mario Bros.', 1980, false);

-- INSERT INTO platforms_games_compatibility (platform_id, game_id) VALUES(1, 1);

INSERT INTO accessory_types (name, description) VALUES('controllers', 'standard button-and-joy-stick type');
INSERT INTO accessory_types (name, description) VALUES('output cords', 'cords that runs from the back of a system to a display device');
INSERT INTO accessory_types (name, description) VALUES('other input devices', 'any device (not of the standard controller variety) used for making game input, such as a microphone or game instrument');
INSERT INTO accessory_types (name, description) VALUES('storage device', 'devices that provide storage for game or save data');
INSERT INTO accessory_types (name, description) VALUES('performance enhancers', 'devices that enable better system performance, such as RAM extenders');
INSERT INTO accessory_types (name, description) VALUES('adapters', 'devices which allow input or output not natively supported by systems');
INSERT INTO accessory_types (name, description) VALUES('game modifiers', 'devices which boot games with traditionally unavailable options included, such as Game Shark or Action Replay');
INSERT INTO accessory_types (name, description) VALUES('power suppliers', 'items used to provide a standard, alternative, or backup source of power');
INSERT INTO accessory_types (name, description) VALUES('on-device screens', 'screens which attach directly to systems, making play possible without a TV or monitor');
INSERT INTO accessory_types (name, description) VALUES('material output devices', 'devices which output real-world items such as photo prints');

-- INSERT INTO accessories (name, type, year_first_release, is_first_party) VALUES('GameCube controller', 1, 2001, true);

-- INSERT INTO games_accessories_compatibility (game_id, accessory_id) VALUES(1, 1);

-- INSERT INTO platforms_accessories_compatibility (platform_id, accessory_id) VALUES(1, 1);

-- INSERT INTO accessory_variations (accessory_id, description) VALUES(1, 'symphonic green color for Tales of Symphonia');

-- INSERT INTO accessory_variations_colors (accessory_variation_id, color_id) VALUES(1, 8);

INSERT INTO characters (name, name_disambiguation, from_what) VALUES('Mario', 'Super Mario', 'Super Mario Bros. franchise');
INSERT INTO characters (name, name_disambiguation, from_what) VALUES('Luigi', NULL, 'Super Mario Bros. franchise');
INSERT INTO characters (name, name_disambiguation, from_what) VALUES('Peach', 'Princess Peach', 'Super Mario Bros. franchise');
INSERT INTO characters (name, name_disambiguation, from_what) VALUES('Daisy', 'Princess Daisy', 'Super Mario Bros. franchise');
INSERT INTO characters (name, name_disambiguation, from_what) VALUES('Yoshi', NULL, 'Super Mario Bros. franchise');
INSERT INTO characters (name, name_disambiguation, from_what) VALUES('Bowser', NULL, 'Super Mario Bros. franchise');

INSERT INTO characters (name, name_disambiguation, from_what) VALUES('Bulbasaur', NULL, 'Pokemon franchise');
INSERT INTO characters (name, name_disambiguation, from_what) VALUES('Ivysaur', NULL, 'Pokemon franchise');
INSERT INTO characters (name, name_disambiguation, from_what) VALUES('Venasaur', NULL, 'Pokemon franchise');
INSERT INTO characters (name, name_disambiguation, from_what) VALUES('Charmander', NULL, 'Pokemon franchise');
INSERT INTO characters (name, name_disambiguation, from_what) VALUES('Charmeleon', NULL, 'Pokemon franchise');
INSERT INTO characters (name, name_disambiguation, from_what) VALUES('Charizard', NULL, 'Pokemon franchise');
INSERT INTO characters (name, name_disambiguation, from_what) VALUES('Squirtle', NULL, 'Pokemon franchise');
INSERT INTO characters (name, name_disambiguation, from_what) VALUES('Wartortle', NULL, 'Pokemon franchise');
INSERT INTO characters (name, name_disambiguation, from_what) VALUES('Blastoise', NULL, 'Pokemon franchise');
INSERT INTO characters (name, name_disambiguation, from_what) VALUES('Caterpie', NULL, 'Pokemon franchise');
INSERT INTO characters (name, name_disambiguation, from_what) VALUES('Metapod', NULL, 'Pokemon franchise');
INSERT INTO characters (name, name_disambiguation, from_what) VALUES('Butterfree', NULL, 'Pokemon franchise');
INSERT INTO characters (name, name_disambiguation, from_what) VALUES('Weedle', NULL, 'Pokemon franchise');
INSERT INTO characters (name, name_disambiguation, from_what) VALUES('Kakuna', NULL, 'Pokemon franchise');
INSERT INTO characters (name, name_disambiguation, from_what) VALUES('Beedril', NULL, 'Pokemon franchise');
INSERT INTO characters (name, name_disambiguation, from_what) VALUES('Pikachu', NULL, 'Pokemon franchise');

-- INSERT INTO characters_in_games (character_id, game_id, is_playable, playability_extent) VALUES(1, 2, true, 'through fourth act when point of view switches to');
