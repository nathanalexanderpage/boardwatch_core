import pprint
import re
from bs4 import BeautifulSoup

from boardwatch_models import Listing

pp = pprint.PrettyPrinter(indent=2)

class ResultScraper():
	def __init__(self, soup):
		self.soup = soup
		self.data = {}
		self.scrape_data()

	def __str__(self):
		return self.data

	def scrape_data(self):
		print('This is when a child class (specific to a certain site) would scrape data from each posting using BeautifulSoup.')

class CraigslistResultScraper(ResultScraper):
	def scrape_data(self):
		title_tag = self.soup.find(class_='result-title')
		title_tag_cleaned = re.sub(',', ', ', title_tag.text).strip()
		title_tag_cleaned = re.sub(' {2,}', ' ', title_tag_cleaned)
		self.data['title'] = title_tag_cleaned

		duplicate_remove_chars = [
			r'\?',
			r'\*',
			'!',
			'-',
			',',
			'~',
			'&'
		]

		for char in duplicate_remove_chars:
			str_to_replace_command = char + '{2,}'
			title_tag_cleaned = re.sub(str_to_replace_command, char, title_tag_cleaned)

		if 'data-repost-of' in self.soup.attrs:
			self.data['id'] = self.soup.get('data-repost-of')
		else:
			self.data['id'] = self.soup.get('data-pid')

		self.data['title_massaged'] = title_tag_cleaned
		self.data['url'] = title_tag['href'].strip()
		self.data['datetime'] = self.soup.p.time['datetime'].strip()
		self.data['seller_email'] = None
		self.data['seller_phone'] = None

		if self.soup.find(class_='result-price'):
			self.data['price'] = int(re.sub(',', '', self.soup.find(class_='result-price').text.strip())[1:])
		else:
			self.data['price'] = None

		if self.soup.find(class_='result-hood'):
			self.data['neighborhood'] = self.soup.find(class_='result-hood').text.strip()
		else:
			self.data['neighborhood'] = None

class CraigslistPostScraper(ResultScraper):
	def scrape_data(self):
		self.data['seller_email'] = None
		self.data['seller_phone'] = None
		self.data['map_longitude'] = None
		self.data['map_latitude'] = None

		mapbox = self.soup.find(id='map')

		if mapbox is not None:
			self.data['map_longitude'] = mapbox['data-longitude']
			self.data['map_latitude'] = mapbox['data-latitude']
			self.data['map_data_accuracy_score'] = mapbox['data-accuracy']

		main_section = self.soup.find(class_='userbody')
		figure = main_section.find('figure')

		pics = []

		if figure:
			pix_quantity = int(self.soup.find(class_='slider-info').text.split(' ')[3])
			if pix_quantity > 1:
				pix = self.soup.find_all(class_='thumb')
				for pic in pix:
					pics.append(pic['href'])
			else:
				pics.append(figure.find('img')['src'])

		print(pics)

		self.data['condition'] = None
		self.data['manufacturer'] = None
		self.data['model'] = None
		attrs_group = self.soup.find(class_='attrgroup')

		if attrs_group:
			attrs = attrs_group.find_all('span')
			for attr in attrs:
				if attr.name == 'span':
					if 'condition:' in attr.text:
						self.data['condition'] = attr.find('b').text.strip()
					if 'make / manufacturer:' in attr.text:
						self.data['manufacturer'] = attr.find('b').text.strip()
					if 'model name / number:' in attr.text:
						self.data['model'] = attr.find('b').text.strip()

		posting_body = self.soup.find(id='postingbody')
		qr_code_text = posting_body.find(class_='print-information print-qrcode-container').text
		self.data['body'] = posting_body.text[len(qr_code_text):].strip()
		post_info_tags = self.soup.find_all(class_='postinginfo')
		self.data['native_id'] = None
		
		for tag in post_info_tags:
			if tag.name == 'p':
				if 'post id:' in tag.text:
					self.data['native_id'] = tag.text[len('post id:'):].strip()
		pp.pprint(self.data)


if __name__ == '__main__':
	print('running ' + __file__)

	res_html = """
	<li class="result-row" data-pid="6992715594" data-repost-of="6950119461">
		<a class="result-image gallery" data-ids="1:00J0J_84quTTLAkBV,1:00a0a_eEsM9B5sLPu,1:00m0m_6bXfaKWFLhW,1:00L0L_cDPr6i9y1YO,1:00D0D_FJKLc3jGxR,1:00z0z_eYwvVsdLg0i,1:00k0k_hBYChJrKyBI,1:00W0W_9ke9RDKvCSc,1:00707_koGBZcPOTFO,1:01717_4YSrlyBc6Ir,1:00S0S_bb3JvNplCNU,1:00N0N_kWEOOzI5JhL,1:00303_4FWvCDAjT9s,1:00m0m_8Onmj9Q45C9,1:00505_5smR9RotjqC,1:00A0A_B1aiM9rfyf,1:00l0l_8GMQe38aCC0,1:00K0K_dM64X8rLQVZ,1:00f0f_7LZLsVkxCcU,1:00t0t_az2WSJscJ04,1:00707_gV9eDUVGDrF,1:00b0b_2CsI03kJPD5,1:00j0j_68AEoMBARzm,1:01414_cqsjoqFQvZg" href="https://seattle.craigslist.org/see/vgm/d/seahurst-xbox-original-console-all/6992715594.html">
			<span class="result-price">
				$50
			</span>
		</a>
		<p class="result-info">
			<span class="icon icon-star" role="button">
				<span class="screen-reader-text">
					favorite this post
				</span>
			</span>
			<time class="result-date" datetime="2019-10-16 17:42" title="Wed 16 Oct 05:42:37 PM">
				Oct 16
			</time>
			<a class="result-title hdrlnk" data-id="6992715594" href="https://seattle.craigslist.org/see/vgm/d/seahurst-xbox-original-console-all/6992715594.html">
				XBOX Original Console, All Wires, Dance Mat and 2 Controllers
			</a>
			<span class="result-meta">
				<span class="result-price">
					$50
				</span>
				<span class="result-hood">
					(Burien)
				</span>
				<span class="result-tags">
					<span class="pictag">
						pic
					</span>
				</span>
				<span class="banish icon icon-trash" role="button">
					<span class="screen-reader-text">
						hide this posting
					</span>
				</span>
				<span aria-hidden="true" class="unbanish icon icon-trash red" role="button">
				</span>
				<a class="restore-link" href="#">
					<span class="restore-narrow-text">
						restore
					</span>
					<span class="restore-wide-text">
						restore this posting
					</span>
				</a>
			</span>
		</p>
	</li>
	"""
	res_soup = BeautifulSoup(res_html, 'html.parser')
	result = ResultScraper(res_soup)
	result2 = CraigslistResultScraper(res_soup)