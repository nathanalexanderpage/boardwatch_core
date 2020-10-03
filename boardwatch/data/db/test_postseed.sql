SELECT
    p.name as platform,
    pf.name as platform_family,
    png.name as name_group,
    gen.id as gen
    FROM platforms as p
    JOIN platform_families as pf ON pf.id = p.platform_family_id
    LEFT JOIN platform_name_groups as png ON png.id = p.name_group_id
    JOIN generations as gen ON gen.id = pf.generation;

SELECT
    png.name as name_group,
    pf.name as platform_family,
    p.name as platform,
    gen.id as gen,
    pe.name as edition,
    pe.official_color as official_color
    FROM platforms as p
    JOIN platform_families as pf ON pf.id = p.platform_family_id
    LEFT JOIN platform_name_groups as png ON png.id = p.name_group_id
    JOIN generations as gen ON gen.id = pf.generation
    JOIN platform_editions as pe ON pe.platform_id = p.id
    ORDER BY gen, name_group, platform_family, platform;

SELECT
    pe.id as id,
    pe.name as name,
    pe.official_color as official_color,
    pe.has_matte as has_matte,
    pe.has_transparency as has_transparency,
    pe.has_gloss as has_gloss,
    pe.note as note,
    pe.image_url as image_url
    FROM platforms as p
    JOIN platform_editions as pe ON pe.platform_id = p.id
    ORDER BY p.name, name, official_color;

SELECT pe.id as id, STRING_AGG(c.name,', ') as colors
    FROM platform_editions as pe
    JOIN colors_platform_editions as cpe ON cpe.platform_edition_id = pe.id
    JOIN colors as c ON c.id = cpe.color_id
    GROUP BY pe.id
    ORDER BY pe.id;

SELECT
    pe.id as id,
    pe.name as name,
    pe.official_color as official_color,
    pe.has_matte as has_matte,
    pe.has_transparency as has_transparency,
    pe.has_gloss as has_gloss,
    pe.note as note,
    pe.image_url as image_url,
    x.colors,
    p.name as platform_name
    FROM platforms as p
    JOIN platform_editions as pe ON pe.platform_id = p.id
    JOIN
        (SELECT pe.id as id, STRING_AGG(c.name,', ') as colors
        FROM platform_editions as pe
        JOIN colors_platform_editions as cpe ON cpe.platform_edition_id = pe.id
        JOIN colors as c ON c.id = cpe.color_id
        GROUP BY pe.id
        ORDER BY pe.id)
    as x ON x.id = pe.id
    ORDER BY p.name, name, official_color;
