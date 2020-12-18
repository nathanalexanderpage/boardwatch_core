INSERT INTO users
    (
        username,
        email,
        password
    )
    VALUES(
        'testuser',
        'testuser@test.user',
        crypt('testuser', gen_salt('bf'))
    );

INSERT INTO watchlist_platform_editions
    (
        user_id,
        platform_edition_id
    )
    VALUES(
        (SELECT id FROM users WHERE username = 'testuser' LIMIT 1),
        (SELECT id FROM platform_editions WHERE platform_id = (
            SELECT id FROM platforms WHERE model_no = 'SNS-001'
        ) LIMIT 1)
    );

SELECT
    wpe.user_id as user_id,
    pf.name AS platform_family,
    p.name AS platform,
    wpe.platform_edition_id as watched_platform_edition_id,
    pe.name AS edition_name,
    pe.official_color AS official_color,
    x.colors AS colors
    FROM watchlist_platform_editions as wpe
    JOIN platform_editions AS pe ON pe.id = wpe.platform_edition_id
    JOIN platforms AS p ON pe.platform_id = p.id
    JOIN platform_families AS pf ON pf.id = p.platform_family_id
    LEFT JOIN platform_name_groups AS png ON png.id = p.name_group_id
    JOIN generations AS gen ON gen.id = pf.generation
    JOIN
        (SELECT pe.id AS id, STRING_AGG(c.name,', ') AS colors
        FROM platform_editions AS pe
        JOIN colors_platform_editions AS cpe ON cpe.platform_edition_id = pe.id
        JOIN colors AS c ON c.id = cpe.color_id
        GROUP BY pe.id
        ORDER BY pe.id)
    AS x ON x.id = pe.id
    ORDER BY user_id, gen.id, png.name, platform_family, platform;
