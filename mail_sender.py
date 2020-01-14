import os
import smtplib
from board_sites import board_sites
from console_data_resource import *
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from email.MIMEImage import MIMEImage
from match_finder import *
from soup_maker import *
from string import Template

import pprint
pp = pprint.PrettyPrinter(indent=2)

cl_results_scraper = CraigslistSoupMaker()
test_parsed_results = cl_results_scraper.make_soup()

pp.pprint(test_parsed_results)
pp.pprint(ps1)

matcher = ConsoleMatchFinder(ps1, {})
matches = [result for result in test_parsed_results if matcher.assess_match(result)]

usable_sites = [site for site in board_sites if site['is_supported']]

pp.pprint(matches)

def generate_message_text(listings):
	message_text_matches = ''
	for site in usable_sites:
		site_message = '\n\nListings from ' + site['name'] + ' (' + site['url'] + '):'
		listing_ct = 1
		for listing in listings:
			site_message = site_message + '\n' + str(listing_ct) + '. ' + listing['title'] + '\n' + listing['url']
			listing_ct += 1
		message_text_matches = message_text_matches + site_message
	return message_text_matches

def generate_message_html(listings):
	message_text_matches = ''

	for site in usable_sites:
		site_message = '<h2>Listings from ' + site['name'] + ' (' + site['url'] + '):</h2>\n<ul style="padding: 0; list-style: none;">'
		listing_ct = 1
		for listing in listings:
			listing_no = str(listing_ct)
			listing_title = listing['title']
			listing_url = listing['url']
			listing_datetime = listing['datetime']
			listing_price = '$' + str(listing['price'])
			site_message = site_message + '\n<li style="margin: 2px 0;border: 3px solid lightgrey;padding: 1em;background-color: #f4f4f4;">\n<span style="font-size: 1.15em;">' + listing_no + '. <a href="' + listing_url + '" style="color: black;">' + listing_title + '</a>' + ' – <span style="color: green; font-weight: bold;">' + listing_price + '</span>\n</span>\n<p><span style="color: #563900;"><time>' + listing_datetime + '</time></span></p>\n</li>'
			listing_ct += 1
		site_message = site_message + '\n</ul>'
		message_text_matches = message_text_matches + site_message
	return message_text_matches


message_listings_text = generate_message_text(matches)
message_listings_html = generate_message_html(matches)

load_dotenv()
GMAIL_ADDRESS = os.getenv('GMAIL_ADDRESS')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')
HOST_ADDRESS = os.getenv('HOST_ADDRESS')
TLS_PORT = os.getenv('TLS_PORT')

def get_contacts(filename):
	names = []
	emails = []
	with open(filename, mode='r', encoding='utf-8') as contacts_file:
		for contact in contacts_file:
			names.append(contact.split()[0])
			emails.append(contact.split()[1])
	return names, emails

def read_template(filename):
	with open(filename, 'r', encoding='utf-8') as template_file:
		template_file_content = template_file.read()
	return Template(template_file_content)

def py_mail():
	names, emails = get_contacts('contacts.txt')
	message_html_template = read_template('mail_message.html')
	message_text_template = read_template('mail_message.txt')

	print(names)
	print(emails)

	smtp = smtplib.SMTP(host=HOST_ADDRESS, port=TLS_PORT)
	smtp.starttls()
	smtp.login(GMAIL_ADDRESS, GMAIL_PASSWORD)

	for name, email in zip(names, emails):
		print('SENDING to ' + email)
		msg = MIMEMultipart('alternative')
		message_html = message_html_template.substitute(RECIPIENT=name, MATCHING_POSTS=message_listings_html)
		message_text = message_text_template.substitute(RECIPIENT=name, MATCHING_POSTS=message_listings_text)

		msg['From'] = GMAIL_ADDRESS
		msg['To'] = email
		msg['Subject'] = 'Craigswatch'
		msg.preamble = message_text.encode('ascii', 'ignore').decode('unicode_escape')

		msg.attach(MIMEText(message_html.encode('utf-8'), _subtype='html', _charset='UTF-8'))

		smtp.send_message(msg)
		del msg
		print('\t\tSENT')
	smtp.quit()

if __name__ == '__main__':
	message_articles_html_test = """
	<p>Recipient,</p>

	<p>Here are your requested post notifications.</p>

	<h2>Posts from Craigslist:</h2>

	<details>
		<summary>This is what you want to show before expanding</summary>
		<p>This is where you put the details that are shown once expanded</p>
	</details>

	<p>[ { 'datetime': '2019-10-18 00:56',
		'neighborhood': '(Kirkland/Kingsgate/Northgate/Greenlake)',
		'price': 25,
		'title': 'titan sony playstation 3 ps3 macro recording controller',
		'url': 'https://seattle.craigslist.org/see/vgm/d/redmond-titan-sony-playstation-3-ps3/6995956982.html'},
	{ 'datetime': '2019-10-17 22:13',
		'neighborhood': '(Seattle)',
		'price': 25,
		'title': '2 yakuza games ps4',
		'url': 'https://seattle.craigslist.org/see/vgm/d/seattle-2-yakuza-games-ps4/6990700959.html'},
	{ 'datetime': '2019-10-17 20:03',
		'neighborhood': None,
		'price': 25,
		'title': 'red dead redemption 2 - ps4',
		'url': 'https://seattle.craigslist.org/see/vgm/d/seattle-red-dead-redemption-2-ps4/7001875235.html'},
	{ 'datetime': '2019-10-17 17:43',
		'neighborhood': '(8917 Lake City Way NE)',
		'price': 55,
		'title': 'sony playstation 3 slim video game console bundle cech-3001a  '
				'ps3',
		'url': 'https://seattle.craigslist.org/see/vgm/d/seattle-sony-playstation-3-slim-video/6997816751.html'},
	{ 'datetime': '2019-10-17 17:11',
		'neighborhood': '(Gig Harbor)',
		'price': 50,
		'title': 'playstation 2 games',
		'url': 'https://seattle.craigslist.org/tac/vgm/d/gig-harbor-playstation-2-games/7000123555.html'},
	{ 'datetime': '2019-10-17 15:55',
		'neighborhood': '(Federal Way)',
		'price': 5,
		'title': 'ps4 slim wall mount brackets',
		'url': 'https://seattle.craigslist.org/see/vgm/d/federal-way-ps4-slim-wall-mount-brackets/6998777498.html'},
	{ 'datetime': '2019-10-17 15:01',
		'neighborhood': '(Chehalis)',
		'price': 20,
		'title': 'brand new shrink wrapped ps3 games',
		'url': 'https://seattle.craigslist.org/oly/vgm/d/chehalis-brand-new-shrink-wrapped-ps3/6994182722.html'},
	{ 'datetime': '2019-10-17 11:37',
		'neighborhood': '(Bremerton FairGrounds)',
		'price': 0,
		'title': 'playstation 4.   games.',
		'url': 'https://seattle.craigslist.org/kit/vgm/d/bremerton-playstation-4-games/6998229646.html'},
	{ 'datetime': '2019-10-17 11:30',
		'neighborhood': '(Seattle)',
		'price': 40,
		'title': 'playstation 2 games lot + case',
		'url': 'https://seattle.craigslist.org/see/vgm/d/seattle-playstation-2-games-lot-case/6994224247.html'},
	{ 'datetime': '2019-10-17 11:20',
		'neighborhood': '(Kent)',
		'price': 250,
		'title': 'sony playstation 4 ps4 slim 1tb console cuh-2215b jet black',
		'url': 'https://seattle.craigslist.org/skc/vgm/d/kent-sony-playstation-4-ps4-slim-1tb/6996687777.html'},
	{ 'datetime': '2019-10-17 11:10',
		'neighborhood': '(Kent)',
		'price': 45,
		'title': 'sony dualshock wireless controller for playstation 4 black '
				'cuh-zct2u',
		'url': 'https://seattle.craigslist.org/skc/vgm/d/kent-sony-dualshock-wireless-controller/6995521460.html'},
	{ 'datetime': '2019-10-17 10:31',
		'neighborhood': '(Kent)',
		'price': 150,
		'title': 'sony playstation 3 ps3 80gb console 4-usb port backward '
				'compatible',
		'url': 'https://seattle.craigslist.org/skc/vgm/d/kent-sony-playstation-3-ps3-80gb/6994593255.html'},
	{ 'datetime': '2019-10-17 09:52',
		'neighborhood': '(Redmond)',
		'price': 350,
		'title': 'ps4 pro - trade for xbox one x',
		'url': 'https://seattle.craigslist.org/est/vgm/d/redmond-ps4-pro-trade-for-xbox-one/6995428895.html'},
	{ 'datetime': '2019-10-17 08:55',
		'neighborhood': '(GIG HARBOR)',
		'price': 50,
		'title': 'playstation 2 games',
		'url': 'https://seattle.craigslist.org/tac/vgm/d/gig-harbor-playstation-2-games/7001457076.html'},
	{ 'datetime': '2019-10-17 08:47',
		'neighborhood': '(Seattle)',
		'price': 10,
		'title': 'ps3 star wars disney infinity darth vader skywalker playstation '
		'url': 'https://seattle.craigslist.org/see/vgm/d/seattle-ps3-star-wars-disney-infinity/6998139382.html'},
	{ 'datetime': '2019-10-17 08:21',
		'neighborhood': '(Puyallup)',
		'price': 5,
		'title': "playstation game-miss spider's tea party",
		'url': 'https://seattle.craigslist.org/tac/vgm/d/puyallup-playstation-game-miss-spiders/7001430464.html'},
	{ 'datetime': '2019-10-17 01:36',
		'url': 'https://seattle.craigslist.org/est/vgm/d/duvall-guitar-hero-game-and-guitar-for/6996898299.html'},
	{ 'datetime': '2019-10-17 01:34',
		'neighborhood': '(Duvall)',
		'price': 20,
		'url': 'https://seattle.craigslist.org/est/vgm/d/duvall-mad-catz-xbox-gamecube-ps2/6996434820.html'},
	{ 'datetime': '2019-10-17 01:18',
		'neighborhood': None,
		'price': 0,
		'title': 'ps4,xbox one,nintendo switch parts and repairs',
		'url': 'https://seattle.craigslist.org/sno/vgm/d/marysville-ps4xbox-onenintendo-switch/6999817228.html'},
	{ 'datetime': '2019-10-17 01:17',
		'price': 0,
		'title': 'ps3 ps4 xbox one 360 parts blu ray drives hard drives power '
				'supplies',
		'url': 'https://seattle.craigslist.org/sno/vgm/d/ps3-ps4-xbox-one-360-parts-blu-ray/6999819929.html'},
	{ 'datetime': '2019-10-17 01:17',
		'neighborhood': None,
		'price': 35,
	{ 'datetime': '2019-10-17 01:17',
		'neighborhood': None,
		'price': 20,
				'sale.',
		'url': 'https://seattle.craigslist.org/sno/vgm/d/marysville-have-broken-xbox-oneps4-pro/6999817274.html'},
	{ 'datetime': '2019-10-17 01:16',
		'neighborhood': None,
		'price': 245,
		'title': 'sony playstation vr - worlds bundle ps4 $460 retail',
		'url': 'https://seattle.craigslist.org/sno/vgm/d/marysville-sony-playstation-vr-worlds/6999817192.html'},
	{ 'datetime': '2019-10-16 23:02',
		'neighborhood': '(Silverdale)',
		'price': 45,
		'title': 'psvr aim controller + firewall bundle - used',
		'url': 'https://seattle.craigslist.org/kit/vgm/d/silverdale-psvr-aim-controller-firewall/7001269698.html'},
	{ 'datetime': '2019-10-16 22:20',
		'neighborhood': '(Kent)',
		'price': 50,
		'title': 'ps2 slim with 2 controllers',
		'url': 'https://seattle.craigslist.org/see/vgm/d/kent-ps2-slim-with-2-controllers/7001262900.html'},
	{ 'datetime': '2019-10-16 21:40',
		'neighborhood': None,
		'price': 220,
		'title': 'sony playstation 4 - 500 gb slim - glacier white + accessories',
		'url': 'https://seattle.craigslist.org/skc/vgm/d/renton-sony-playstation-gb-slim-glacier/6994262957.html'}]</p>

	<p></p>
	<p></p>
	<p>-Nathan Mailbot</p>
	"""

	py_mail()