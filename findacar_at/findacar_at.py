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

	post_code = 'gu216yl'
	min_price = 2500
	max_price = 3600
	min_mileage = 0
	max_mileage = 57000
	min_year = 2010
	max_year = 2017
	this_year = 2020
	
	search_url = r'https://www.autotrader.co.uk/car-search?postcode={post_code}&radius=15&price-from={min_price}&price-to={max_price}&year-from={min_year}&year-to={max_year}&maximum-mileage={max_mileage}&fuel-type=Petrol&quantity-of-doors=5&fuel-consumption=OVER_50'.format(
		post_code = post_code,
		min_price = min_price,
		max_price = max_price,
		max_mileage = max_mileage,
		min_year = min_year,
		max_year = max_year,
	)
	
	min_age = this_year - max_year
	max_age = this_year - min_year
	
	price_range = max_price - min_price
	age_range = max_age - min_age
	mileage_range = max_mileage - min_mileage

	print("URL:", search_url)
	print("Get page count ...")
	r = requests.get(search_url)
	search_soup = bs4.BeautifulSoup(r.content, features="html.parser")
	page_count = int(
		[li.find_all('strong')[1].text for li in search_soup.find_all('li') if 'class' in li.attrs and 'paginationMini__count' in li['class']][0]
	)
	print('Number of pages:', page_count)

	ids = []
	cars = []
	for page in range(1, page_count + 1):
		print("Get ids from page {} ...".format(page))
		r = requests.get(search_url+'&page={}'.format(page))		
		search_soup = bs4.BeautifulSoup(r.content, features="html.parser")
		
		this_page_ids = [li['id'] for li in search_soup.find_all('li') if 'class' in li.attrs and 'search-page__result' in li['class'] and 'data-is-promoted-listing' not in li.attrs and 'data-is-ymal-listing' not in li.attrs]

		for id_ in this_page_ids:
			id_li = search_soup.find('li', id = id_)
			
			spec_lis = id_li.find_all('li', class_ = False)
			if 'CAT' in spec_lis[0].text:
				continue

			price_div = id_li.find('div', class_ = 'vehicle-price')
			if price_div is not None:
				price = int(price_div.text.replace('£', '').replace(',', ''))
			else:
				price_div = id_li.find('div', class_ = 'advert-card-pricing__price')
				price = int(price_div.text.replace('£', '').replace(',', ''))

			year = int(spec_lis[0].text.split(' ')[0])
			mileage = int(spec_lis[2].text.replace(' miles', '').replace(',', ''))
			distance = int(id_li.get('data-distance-value').split(' ')[0])

			age = this_year-year
			norm_price = (price - min_price)/price_range
			norm_age = (age - min_age)/age_range
			norm_mileage = (mileage - min_mileage)/mileage_range
			cars.append(
				{
					'id' : id_,
					'price' : price,
					'year' : year,
					'mileage' : mileage,
					'distance' : distance,
					'norm_price' : norm_price,
					'norm_age' : norm_age,
					'norm_mileage' : norm_mileage,
					'score' : 1/6*(2*norm_price + 3*norm_mileage + 1*norm_age),
				}
			)

		ids.extend(this_page_ids)

	sorted_cars = sorted(cars, key=lambda car: car['score'])

	for car in sorted_cars:
		webbrowser.open('https://www.autotrader.co.uk/car-details/{}'.format(car['id']))
		print(car)
		import IPython; IPython.embed(colors='Neutral')

## -------- SOMETHING WENT WRONG -----------------------------	
except:

	import traceback
	LOG.error("Something went wrong! Exception details:\n{}".format(traceback.format_exc()))
	import IPython; IPython.embed(colors='Neutral')

## -------- GIVE THE USER A CHANCE TO READ MESSAGES-----------
finally:
	
	pass
