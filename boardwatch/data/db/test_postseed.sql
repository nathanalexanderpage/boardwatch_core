SELECT
	p.name AS platform,
	pf.name AS platform_family,
	png.name AS name_group,
	gen.id AS gen
	FROM platforms AS p
	JOIN platform_families AS pf ON pf.id = p.platform_family_id
	LEFT JOIN platform_name_groups AS png ON png.id = p.name_group_id
	JOIN generations AS gen ON gen.id = pf.generation;

SELECT
	png.name AS name_group,
	pf.name AS platform_family,
	p.name AS platform,
	gen.id AS gen,
	pe.name AS edition,
	pe.official_color AS official_color
	FROM platforms AS p
	JOIN platform_families AS pf ON pf.id = p.platform_family_id
	LEFT JOIN platform_name_groups AS png ON png.id = p.name_group_id
	JOIN generations AS gen ON gen.id = pf.generation
	JOIN platform_editions AS pe ON pe.platform_id = p.id
	ORDER BY gen, name_group, platform_family, platform;

SELECT
	pe.id AS id,
	pe.name AS name,
	pe.official_color AS official_color,
	pe.has_matte AS has_matte,
	pe.has_transparency AS has_transparency,
	pe.has_gloss AS has_gloss,
	pe.note AS note,
	pe.image_url AS image_url
	FROM platforms AS p
	JOIN platform_editions AS pe ON pe.platform_id = p.id
	ORDER BY p.name, name, official_color;

SELECT pe.id AS id, STRING_AGG(c.name,', ') AS colors
	FROM platform_editions AS pe
	JOIN colors_platform_editions AS cpe ON cpe.platform_edition_id = pe.id
	JOIN colors AS c ON c.id = cpe.color_id
	GROUP BY pe.id
	ORDER BY pe.id;

SELECT
	pe.id AS id,
	pe.name AS name,
	pe.official_color AS official_color,
	pe.has_matte AS has_matte,
	pe.has_transparency AS has_transparency,
	pe.has_gloss AS has_gloss,
	pe.note AS note,
	pe.image_url AS image_url,
	x.colors,
	p.id AS platform_id
	-- p.name AS platform_name
	FROM platforms AS p
	JOIN platform_editions AS pe ON pe.platform_id = p.id
	JOIN
		(SELECT pe.id AS id, STRING_AGG(c.name,', ') AS colors
		FROM platform_editions AS pe
		JOIN colors_platform_editions AS cpe ON cpe.platform_edition_id = pe.id
		JOIN colors AS c ON c.id = cpe.color_id
		GROUP BY pe.id
		ORDER BY pe.id)
	AS x ON x.id = pe.id
	ORDER BY p.id, name, official_color;

SELECT
	id,
	native_id,
	title,
	body,
	price,
	url,
	date_posted,
	date_scraped,
	board_id
	FROM listings
	WHERE is_scanned = FALSE AND date_posted >= ((now() AT TIME ZONE 'utc') - interval '1 day');
