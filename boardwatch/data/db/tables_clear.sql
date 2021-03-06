DELETE FROM watchlist_accessory_variations WHERE accessory_variation_id > 0;
DELETE FROM watchlist_accessories WHERE accessory_id > 0;
DELETE FROM watchlist_games WHERE game_id > 0;
DELETE FROM watchlist_platform_editions WHERE platform_edition_id > 0;
DELETE FROM watchlist_platforms WHERE platform_id > 0;
DELETE FROM listings_accessory_variations WHERE accessory_variation_id > 0;
DELETE FROM listings_accessories WHERE accessory_id > 0;
DELETE FROM listings_games WHERE game_id > 0;
DELETE FROM listings_platform_editions WHERE platform_edition_id > 0;
DELETE FROM listings_platforms WHERE platform_id > 0;
DELETE FROM accessories_platforms_compatibility WHERE platform_id > 0;
DELETE FROM colors_platform_editions WHERE color_id > 0;
DELETE FROM games_platforms_compatibility WHERE game_id > 0;
DELETE FROM accessories_games_compatibility WHERE accessory_id > 0;
DELETE FROM companies_platforms WHERE company_id > 0;
DELETE FROM platform_editions WHERE id > 0;
DELETE FROM addon_platforms WHERE id > 0;
DELETE FROM platforms WHERE id > 0;
DELETE FROM platform_families WHERE id > 0;
DELETE FROM platform_name_groups WHERE id > 0;
DELETE FROM generations WHERE id > 0;
DELETE FROM colors WHERE id > 0;
DELETE FROM game_families_games WHERE game_id > 0;
DELETE FROM game_series_games WHERE game_id > 0;
DELETE FROM games WHERE id > 0;
DELETE FROM game_families WHERE id > 0;
DELETE FROM game_series WHERE id > 0;
DELETE FROM accessory_variations_colors WHERE color_id > 0;
DELETE FROM accessory_variations WHERE id > 0;
DELETE FROM accessories WHERE id > 0;
DELETE FROM accessory_types WHERE id > 0;
DELETE FROM characters_in_games WHERE character_id > 0;
DELETE FROM characters WHERE id > 0;
DELETE FROM listings WHERE id IS NOT NULL;
-- DELETE FROM listing_categories WHERE id > 0;
DELETE FROM boards WHERE id > 0;
-- DELETE FROM boards_listing_categories WHERE id > 0;
DELETE FROM company_roles WHERE id > 0;
DELETE FROM companies WHERE id > 0;
DELETE FROM users WHERE id IS NOT NULL;
