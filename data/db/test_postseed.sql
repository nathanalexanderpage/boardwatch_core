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
