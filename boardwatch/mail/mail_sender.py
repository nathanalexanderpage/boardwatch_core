from datetime import datetime
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

load_dotenv()
GMAIL_ADDRESS = os.getenv('GMAIL_ADDRESS')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')
GMAIL_HOST_ADDRESS = os.getenv('GMAIL_HOST_ADDRESS')
GMAIL_TLS_PORT = os.getenv('GMAIL_TLS_PORT')

pp = pprint.PrettyPrinter(indent=2)

class Mailer():
	pe_presences_per_pe = None
	platform_presences_per_platform = None

	def __init__(self, user, platforms, platform_editions, games, accessories):
		self.user = user
		self.platforms = platforms
		if platforms is None:
			self.platforms = list()
		self.platform_editions = platform_editions
		self.games = games
		if games is None:
			self.games = list()
		self.accessories = accessories
		if accessories is None:
			self.accessories = list()

	def generate_message_text(self):
		message_text_matches = ''
		message_text_matches = message_text_matches + 'PLATFORMS & EDITIONS\n\n'

		pp.pprint(Listing.registry)
		for platform in Platform.get_all():
			if platform.id in self.platform_editions or (self.platforms and platform.id in self.platforms):
				message_text_per_platform = ''

				# ----- Platform Name -----
				message_text_per_platform = message_text_per_platform + '----- ' + platform.name + ' -----\n'

				if self.platform_editions.get(platform.id):
					for edition_id in self.platform_editions.get(platform.id):
						edition = PlatformEdition.get_by_id(edition_id)

						edition_referencial_name = edition.referencial_name()

						message_text_per_platform = message_text_per_platform + edition_referencial_name + '\n'

						if Mailer.pe_presences_per_pe.get(edition.id):
							for listing_id in Mailer.pe_presences_per_pe.get(edition.id):
								listing = Listing.get_by_id(listing_id)
								# listing title
								message_text_per_platform = message_text_per_platform + '\t' + listing.title + '\n'

								# listing price
								if listing.price is None:
									message_text_per_platform = message_text_per_platform + '\t' + '(price not listed)' + '\n'
								else:
									message_text_per_platform = message_text_per_platform + '\t' + listing.price + '\n'

								# listing link
								message_text_per_platform = message_text_per_platform + '\t' + listing.url + '\n'

								# listing datetime
								message_text_per_platform = message_text_per_platform + '\t' + str(listing.date_posted) + '\n'

								# blank line
								message_text_per_platform = message_text_per_platform + '\t' + '\n'
					message_text_per_platform = message_text_per_platform + '\n'

				message_text_matches = message_text_matches + message_text_per_platform
		return message_text_matches

	def generate_message_html(self):
		message_text_matches = ''
		products_matched_ct = 0

		platforms_and_editions_category_title =  '<h2>PLATFORMS & EDITIONS</h2>\n\n'
		message_text_all_platforms = ''

		for platform in Platform.get_all():
			message_text_this_platform = ''

			if platform.id in self.platform_editions or (self.platforms and platform.id in self.platforms):
				# Platform Name
				this_platform_name = f'\n<h3>{platform.name}</h3>'

				message_text_this_platform_general = ''
				message_text_this_platform_list = ''

				platform_general_list_start = '\n<ul style="padding: 0; list-style: none;">'
				if self.platform_presences_per_platform.get(platform.id):
					listing_ct = 0
					for listing_id in self.platform_presences_per_platform.get(platform.id):
						listing = Listing.get_by_id(listing_id)
						if listing is not None:
							listing_ct += 1

							# listing title
							listing_title = None
							if listing.title is None:
								listing_title = '(untitled)'
							else:
								listing_title = listing.title

							# listing price
							listing_price = None
							if listing.price is None:
								listing_price = '(price not listed)'
							else:
								listing_price = str(listing.price)

							# listing URL
							listing_url = listing.url

							# listing datetime
							listing_datetime = listing.date_posted.strftime('%I:%M%p on %Y-%m-%d')

							message_text_this_platform_list = message_text_this_platform_list + f"""
							\n<li style="margin: 2px 0; border: 3px solid lightgrey; padding: 1em; background-color: #f4f4f4;">
							\n<span style="font-size: 1.15em;">{listing_ct}. <a href="{listing_url}" style="color: black;">{listing_title}</a> – <span style="color: green; font-weight: bold;">{listing_price}</span>
							\n</span>
							\n<p><span style="color: #563900;">Posted <time datetime="{str(listing.date_posted)}">{listing_datetime}</time></span></p>
							\n</li>
							"""
				platform_general_list_end = '\n</ul>'

				if len(message_text_this_platform_list) > 0:
					message_text_this_platform_general = message_text_this_platform_general + f"""{platform_general_list_start}\n{message_text_this_platform_list}\n{platform_general_list_end}"""



				message_text_all_editions = ''

				if self.platform_editions.get(platform.id):
					for edition_id in self.platform_editions.get(platform.id):
						edition = PlatformEdition.get_by_id(edition_id)

						edition_referencial_name = edition.referencial_name()

						message_text_this_edition = ''

						this_edition_name = f'\n<h4>{edition_referencial_name}</h4>'

						message_text_this_edition_listings = ''

						if Mailer.pe_presences_per_pe.get(edition.id):
							listing_ct = 0
							editions_list_start = '\n<ul style="padding: 0; list-style: none;">'

							for listing_id in Mailer.pe_presences_per_pe.get(edition.id):
								listing = Listing.get_by_id(listing_id)

								if listing is not None:
									listing_ct += 1

									# listing title
									listing_title = None
									if listing.title is None:
										listing_title = '(untitled)'
									else:
										listing_title = listing.title

									# listing price
									listing_price = None
									if listing.price is None:
										listing_price = '(price not listed)'
									else:
										listing_price = str(listing.price)

									# listing URL
									listing_url = listing.url

									# listing datetime
									listing_datetime = listing.date_posted.strftime('%I:%M%p on %Y-%m-%d')

									message_text_this_edition_listings = message_text_this_edition_listings + f"""
									\n<li style="margin: 2px 0; border: 3px solid lightgrey; padding: 1em; background-color: #f4f4f4;">
									\n<span style="font-size: 1.15em;">{listing_ct}. <a href="{listing_url}" style="color: black;">{listing_title}</a> – <span style="color: green; font-weight: bold;">{listing_price}</span>
									\n</span>
									\n<p><span style="color: #563900;">Posted <time datetime="{str(listing.date_posted)}">{listing_datetime}</time></span></p>
									\n</li>
									"""

							editions_list_end = '\n</ul>'

						if len(message_text_this_edition_listings) > 0:
							products_matched_ct += 1
							# add edition title
							message_text_this_edition = message_text_this_edition + this_edition_name
							# add edition listings
							message_text_this_edition = message_text_this_edition + editions_list_start + message_text_this_edition_listings + editions_list_end

					if len(message_text_this_edition) > 0:
						# add edition message text
						message_text_all_editions = message_text_all_editions + message_text_this_edition

				if len(message_text_all_editions) > 0 or len(message_text_this_platform_general) > 0:
					# add platform title
					message_text_this_platform = message_text_this_platform + this_platform_name
					if len(message_text_this_platform_general) > 0:
						products_matched_ct += 1
						general_platform_matches_title = f'\n<h4>General</h4>'
						# add platform generic message text
						message_text_this_platform = message_text_this_platform + general_platform_matches_title + message_text_this_platform_general
					if len(message_text_all_editions) > 0:
						# add platform editions message text
						message_text_this_platform = message_text_this_platform + message_text_all_editions
					
			if len(message_text_this_platform) > 0:
				# add platform editions message text
				message_text_all_platforms = message_text_all_platforms + message_text_this_platform
					
		if len(message_text_all_platforms) > 0:
			# add platform & edition category title to mail message
			message_text_matches = message_text_matches + platforms_and_editions_category_title
			# add platform & edition category content to mail message
			message_text_matches = message_text_matches + message_text_all_platforms
		
		return message_text_matches, products_matched_ct

	def read_template(self, filename):
		with open(filename, 'r', encoding='utf-8') as template_file:
			template_file_content = template_file.read()
		return Template(template_file_content)

	def send_mail(self, is_user_mail_html_compatible):
		print('SENDING to ' + self.user.email)
		current_folder = str(pathlib.Path(__file__).resolve().parents[0].absolute())

		if is_user_mail_html_compatible:
			message_listings_html, products_matched_ct = self.generate_message_html()

			if products_matched_ct > 0:
				message_html_template = self.read_template(current_folder + '/mail_message.html')
				message_premable_template = self.read_template(current_folder + '/mail_message_preamble.txt')
				message_html = message_html_template.substitute(RECIPIENT=self.user.username, MATCHING_POSTS=message_listings_html)
				message_preamble = message_premable_template.substitute(RECIPIENT=self.user.username)

				msg = MIMEMultipart('alternative')
				msg['From'] = GMAIL_ADDRESS
				msg['To'] = self.user.email
				msg['Subject'] = f"""New matches for {products_matched_ct} of your watched products"""
				msg.preamble = message_preamble.encode('ascii', 'ignore').decode('unicode_escape')
				msg.attach(MIMEText(message_html.encode('utf-8'), _subtype='html', _charset='UTF-8'))

				smtp = smtplib.SMTP(host=GMAIL_HOST_ADDRESS, port=GMAIL_TLS_PORT)
				smtp.ehlo()
				smtp.starttls()
				smtp.login(GMAIL_ADDRESS, GMAIL_PASSWORD)

				smtp.send_message(msg)
				del msg
				print('\t\tSENT')

				smtp.quit()
			else:
				print(f'skipping User {self.user.id}: no matches\n{self.user.email}')
		else:
			message_listings_text = self.generate_message_text()
			message_text_template = self.read_template(current_folder + '/mail_message.txt')
			message_text = message_text_template.substitute(RECIPIENT=self.user.username, MATCHING_POSTS=message_listings_text)

			msg = EmailMessage()
			msg.set_content(message_text)
			msg['From'] = GMAIL_ADDRESS
			msg['To'] = self.user.email
			msg['Subject'] = 'Craigswatch'

			smtp = smtplib.SMTP(host=GMAIL_HOST_ADDRESS, port=GMAIL_TLS_PORT)
			smtp.ehlo()
			smtp.starttls()
			smtp.login(GMAIL_ADDRESS, GMAIL_PASSWORD)

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

	@classmethod
	def calibrate_platform_presences(cls, platform_presences_per_platform):
		"""
		Add reference to dictionary of applicable PlatformEdition presences.
		"""
		cls.platform_presences_per_platform = platform_presences_per_platform
