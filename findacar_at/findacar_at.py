# -*- coding: utf-8 -*-
"""
	findacar_at
	
	This project is an example of a Python project generated from cookiecutter-python.
"""

## -------- COMMAND LINE ARGUMENTS ---------------------------
## https://docs.python.org/3.7/howto/argparse.html
import argparse
CmdLineArgParser = argparse.ArgumentParser()
CmdLineArgParser.add_argument(
	"-v",
	"--verbose",
	help = "display debug messages in console",
	action = "store_true",
)
CmdLineArgs = CmdLineArgParser.parse_args()

## -------- LOGGING INITIALISATION ---------------------------
import misc
misc.MyLoggersObj.SetConsoleVerbosity(ConsoleVerbosity = {True : "DEBUG", False : "INFO"}[CmdLineArgs.verbose])
LOG, handle_retval_and_log = misc.CreateLogger(__name__)

try:
	
	## -------------------------------------------------------
	## THE MAIN PROGRAM STARTS HERE
	## -------------------------------------------------------	

	import requests
	import bs4
	import webbrowser
	from requests_html import HTMLSession
	
	search_url = r'https://www.autotrader.co.uk/car-search?sort=distance&postcode=gu213bn&radius=15&price-from=2500&price-to=3500&year-from=2010&year-to=2015&maximum-mileage=52000&fuel-type=Petrol&quantity-of-doors=5&fuel-consumption=OVER_50'

	print("Get page count ...")
	r = requests.get(search_url)
	search_soup = bs4.BeautifulSoup(r.content, features="html.parser")
	page_count = int(
		[li.find_all('strong')[1].text for li in search_soup.find_all('li') if 'class' in li.attrs and 'paginationMini__count' in li['class']][0]
	)

	ids = []
	for page in range(page_count):
		print("Get ids from page {} ...".format(page))
		r = requests.get(search_url+'&page={}'.format(page))		
		search_soup = bs4.BeautifulSoup(r.content, features="html.parser")
		ids.extend(
			[li['id'] for li in search_soup.find_all('li') if 'class' in li.attrs and 'search-page__result' in li['class'] and 'data-is-promoted-listing' not in li.attrs and 'data-is-ymal-listing' not in li.attrs]
		)

	car_urls = ['https://www.autotrader.co.uk/car-details/{}'.format(id) for id in ids]
	for car_url in car_urls:
		# webbrowser.open(car_url)
		session = HTMLSession()
		r = session.get(car_url)
		r.html.render()
		car_soup = bs4.BeautifulSoup(r.html.raw_html, features="html.parser")
		
		price = int(
			car_soup.find('h2', class_ = 'price-confidence__price').text.replace('Price £', '').replace(',', '')
		)
		mileage = car_soup.find('span', class_ = 'mileage__distance').text
		age = car_soup.find('p', class_ = 'advert-heading__year-title').text


		It will be quicker to do the scraping from the search page itself instead of the actual car page which needs javascript to be rendered properly.

		import IPython; IPython.embed(colors='Neutral')


## -------- SOMETHING WENT WRONG -----------------------------	
except:

	import traceback
	LOG.error("Something went wrong! Exception details:\n{}".format(traceback.format_exc()))

## -------- GIVE THE USER A CHANCE TO READ MESSAGES-----------
finally:
	
	pass
