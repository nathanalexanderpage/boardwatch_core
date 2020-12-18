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

SELECT * FROM watchlist_platform_editions as wpe
    JOIN users as u ON u.id = wpe.user_id;
