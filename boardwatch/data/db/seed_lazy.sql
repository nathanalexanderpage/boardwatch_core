INSERT INTO boards (name, company_id, board_web_address_base) VALUES('Craigslist', (SELECT id FROM companies WHERE name = 'Craigslist'), 'https://www.craigslist.org/');
