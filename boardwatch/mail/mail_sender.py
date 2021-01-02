from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from email.MIMEImage import MIMEImage
from email.message import EmailMessage
import os
import pathlib
import pprint
import smtplib
from string import Template

from boardwatch_models import Board, Listing, Platform, PlatformEdition, PlatformNameGroup, User
from dotenv import load_dotenv

from boardwatch.common import board_site_enums
from boardwatch.match import profilers
from boardwatch.scrape.soup_maker import CraigslistSoupMaker

load_dotenv()
GMAIL_ADDRESS = os.getenv('GMAIL_ADDRESS')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')
GMAIL_HOST_ADDRESS = os.getenv('GMAIL_HOST_ADDRESS')
GMAIL_TLS_PORT = os.getenv('GMAIL_TLS_PORT')

pp = pprint.PrettyPrinter(indent=2)

# cl_results_scraper = CraigslistSoupMaker()
# test_parsed_results = cl_results_scraper.make_soup()

# pp.pprint(test_parsed_results)

# matcher = PlatformProfiler(ps1, {})
# matches = [result for result in test_parsed_results if matcher.assess_match(result)]

usable_sites = [site for site in board_site_enums.board_sites if site['is_supported']]

# pp.pprint(matches)

class Mailer():
	pe_presences_per_pe = None

	def __init__(self, user, platforms, platform_editions, games, accessories):
		self.user = user
		self.platforms = platforms
		if platforms is None:
			self.platforms = list()
		self.platform_editions = platform_editions
		self.games = games
		self.accessories = accessories

	def generate_message(self, is_user_mail_html_compatible):
		if is_user_mail_html_compatible:
			return self.generate_message_html()
		else:
			return self.generate_message_text()

	def generate_message_text(self):
		message_text_matches = ''

		message_text_matches = message_text_matches + 'PLATFORMS & EDITIONS\n\n'

		print(self.platforms)

		pp.pprint(Listing.registry)
		for platform in Platform.get_all():
			# ?
			if platform.id in self.platform_editions or (self.platforms and platform.id in self.platforms):
				site_message_per_platform = ''

				# ----- Platform Name -----
				site_message_per_platform = site_message_per_platform + '----- ' + platform.name + ' -----\n'

				if self.platform_editions.get(platform.id):
					for edition_id in self.platform_editions.get(platform.id):
						edition = PlatformEdition.get_by_id(edition_id)

						edition_referencial_name = ''

						if edition.name:
							if len(edition_referencial_name) != 0:
								edition_referencial_name = edition_referencial_name + ' '
							edition_referencial_name = edition_referencial_name + edition.name
						if edition.official_color:
							if len(edition_referencial_name) != 0:
								edition_referencial_name = edition_referencial_name + ' '
							edition_referencial_name = edition_referencial_name + edition.official_color
						if len(edition.colors) > 0:
							for color in edition.colors:
								if len(edition_referencial_name) != 0:
									edition_referencial_name = edition_referencial_name + ' '
								edition_referencial_name = edition_referencial_name + color

						site_message_per_platform = site_message_per_platform + edition_referencial_name + '\n'

						if Mailer.pe_presences_per_pe.get(edition.id):
							for listing_id in Mailer.pe_presences_per_pe.get(edition.id):
								listing = Listing.get_by_id(listing_id)
								# listing title
								site_message_per_platform = site_message_per_platform + '\t' + listing.title + '\n'

								# listing price
								if listing.price is None:
									site_message_per_platform = site_message_per_platform + '\t' + '(price not listed)' + '\n'
								else:
									site_message_per_platform = site_message_per_platform + '\t' + listing.price + '\n'

								# listing link
								site_message_per_platform = site_message_per_platform + '\t' + listing.url + '\n'

								# listing datetime
								site_message_per_platform = site_message_per_platform + '\t' + str(listing.date_posted) + '\n'

								# blank line
								site_message_per_platform = site_message_per_platform + '\t' + '\n'
						print(site_message_per_platform)
					site_message_per_platform = site_message_per_platform + '\n'

				message_text_matches = message_text_matches + site_message_per_platform
		return message_text_matches

	def generate_message_html(self):
		message_text_matches = ''
		message_text_matches = message_text_matches + 'PLATFORMS & EDITIONS\n\n'

		print(self.platforms)

		pp.pprint(Listing.registry)
		for platform in Platform.get_all():
			# ?
			if platform.id in self.platform_editions or (self.platforms and platform.id in self.platforms):
				site_message_per_platform = ''

				# ----- Platform Name -----
				site_message_per_platform = site_message_per_platform + '----- ' + platform.name + ' -----\n'

				if self.platform_editions.get(platform.id):
					for edition_id in self.platform_editions.get(platform.id):
						edition = PlatformEdition.get_by_id(edition_id)

						edition_referencial_name = ''

						if edition.name:
							if len(edition_referencial_name) != 0:
								edition_referencial_name = edition_referencial_name + ' '
							edition_referencial_name = edition_referencial_name + edition.name
						if edition.official_color:
							if len(edition_referencial_name) != 0:
								edition_referencial_name = edition_referencial_name + ' '
							edition_referencial_name = edition_referencial_name + edition.official_color
						if len(edition.colors) > 0:
							for color in edition.colors:
								if len(edition_referencial_name) != 0:
									edition_referencial_name = edition_referencial_name + ' '
								edition_referencial_name = edition_referencial_name + color

						site_message_per_platform = site_message_per_platform + edition_referencial_name + '\n'

						if Mailer.pe_presences_per_pe.get(edition.id):
							for listing_id in Mailer.pe_presences_per_pe.get(edition.id):
								f"""
								\n<li style="margin: 2px 0; border: 3px solid lightgrey; padding: 1em; background-color: #f4f4f4;">
								\n<span style="font-size: 1.15em;">{listing_no}. <a href="{listing_url}" style="color: black;">{listing_title}</a> – <span style="color: green; font-weight: bold;">{listing_price}</span>
								\n</span>
								\n<p><span style="color: #563900;"><time>{listing_datetime}</time></span></p>
								\n</li>
								"""
								
								listing = Listing.get_by_id(listing_id)
								# listing title
								site_message_per_platform = site_message_per_platform + '\t' + listing.title + '\n'

								# listing price
								if listing.price is None:
									site_message_per_platform = site_message_per_platform + '\t' + '(price not listed)' + '\n'
								else:
									site_message_per_platform = site_message_per_platform + '\t' + listing.price + '\n'

								# listing link
								site_message_per_platform = site_message_per_platform + '\t' + listing.url + '\n'

								# listing datetime
								site_message_per_platform = site_message_per_platform + '\t' + str(listing.date_posted) + '\n'

								# blank line
								site_message_per_platform = site_message_per_platform + '\t' + '\n'
						print(site_message_per_platform)
					site_message_per_platform = site_message_per_platform + '\n'

				message_text_matches = message_text_matches + site_message_per_platform
		return message_text_matches

	def get_contacts(self, filename):
		names = []
		emails = []
		with open(filename, mode='r', encoding='utf-8') as contacts_file:
			for contact in contacts_file:
				names.append(contact.split()[0])
				emails.append(contact.split()[1])
		return names, emails

	def read_template(self, filename):
		with open(filename, 'r', encoding='utf-8') as template_file:
			template_file_content = template_file.read()
		return Template(template_file_content)

	def send_mail(self, is_user_mail_html_compatible):
		print('SENDING to ' + self.user.email)
		if is_user_mail_html_compatible:
			message_listings_html = self.generate_message_html()
			message_html_template = self.read_template('mail_message.html')
			message_premable_template = self.read_template('mail_message_preamble.txt')

			smtp = smtplib.SMTP(host=GMAIL_HOST_ADDRESS, port=GMAIL_TLS_PORT)
			smtp.starttls()
			smtp.login(GMAIL_ADDRESS, GMAIL_PASSWORD)

			msg = MIMEMultipart('alternative')
			message_html = message_html_template.substitute(RECIPIENT=self.user.name, MATCHING_POSTS=message_listings_html)
			message_preamble = message_premable_template.substitute(RECIPIENT=self.user.name)

			msg['From'] = GMAIL_ADDRESS
			msg['To'] = self.user.email
			msg['Subject'] = 'Craigswatch'
			msg.preamble = message_preamble.encode('ascii', 'ignore').decode('unicode_escape')

			msg.attach(MIMEText(message_html.encode('utf-8'), _subtype='html', _charset='UTF-8'))

			smtp.send_message(msg)
			del msg
			print('\t\tSENT')

			smtp.quit()
		else:
			current_folder = str(pathlib.Path(__file__).resolve().parents[0].absolute())
			print(current_folder)

			message_listings_text = self.generate_message_text()
			# print(message_listings_text)
			message_text_template = self.read_template(current_folder + '/mail_message.txt')

			print(GMAIL_ADDRESS, GMAIL_PASSWORD)

			smtp = smtplib.SMTP(host=GMAIL_HOST_ADDRESS, port=GMAIL_TLS_PORT)
			smtp.starttls()
			smtp.login(GMAIL_ADDRESS, GMAIL_PASSWORD)

			print(self.user.username)

			message_text = message_text_template.substitute(RECIPIENT=self.user.username, MATCHING_POSTS=message_listings_text)
			msg = EmailMessage()
			msg.set_content(message_text)

			msg['From'] = GMAIL_ADDRESS
			msg['To'] = self.user.email
			msg['Subject'] = 'Craigswatch'

			smtp.send_message(msg)
			del msg
			print('\t\tSENT')

			smtp.quit()

	@classmethod
	def calibrate_pe_presences(cls, pe_presences_per_pe):
		"""
		Add reference to dictionary of applicable PlatformEdition presences.
		"""
		cls.pe_presences_per_pe = pe_presences_per_pe
