SELECT p.name, pe.name, pe.official_color as color, l.title, l.body FROM platform_editions as pe JOIN platforms as p ON p.id = pe.platform_id JOIN listings_platform_editions as lpe ON lpe.platform_edition_id = pe.id JOIN listings as l ON l.id = lpe.listing_id;

SELECT p.name, l.title, l.body FROM platforms as p JOIN listings_platforms as lp ON lp.platform_id = p.id JOIN listings as l ON l.id = lp.listing_id;
