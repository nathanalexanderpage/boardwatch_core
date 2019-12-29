-- INSERT INTO table (column, column, column, column, column, column, column) VALUES('pink', 'pink', 'pink', 'pink', 'pink', 'pink', 'pink');

-- INSERT INTO platforms (name, platform_family, name_group, model_no, storage_capacity, description, disambiguation, relevance) VALUES('GameCube', 'FK', 'FK', 'DOL-001', 'pink', 'Nintendo''s ______th home console, debuted in', 'the original GameCube', 10);

-- INSERT INTO platform_editions (name, official_color, has_matte, has_transparency, has_gloss, note, image_url_filename) VALUES(NULL, 'Indigo', false, false, false, NULL, NULL);

-- INSERT INTO platform_editions_colors (platform_edition_id, color_id) VALUES(1, 1);

-- INSERT INTO games (name, year_first_release, is_bootleg) VALUES('Super Mario Bros.', 1980, false);

-- INSERT INTO platforms_games_compatibility (platform_id, game_id) VALUES(1, 1);

-- INSERT INTO accessories (name, type, year_first_release, is_first_party) VALUES('GameCube controller', 1, 2001, true);

-- INSERT INTO games_accessories_compatibility (game_id, accessory_id) VALUES(1, 1);

-- INSERT INTO platforms_accessories_compatibility (platform_id, accessory_id) VALUES(1, 1);

-- INSERT INTO accessory_variations (accessory_id, description) VALUES(1, 'symphonic green color for Tales of Symphonia');

-- INSERT INTO accessory_variations_colors (accessory_variation_id, color_id) VALUES(1, 8);

-- INSERT INTO characters_in_games (character_id, game_id, is_playable, playability_extent) VALUES(1, 2, true, 'through fourth act when point of view switches to first person');
