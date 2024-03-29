# importing libraries
from bs4 import BeautifulSoup
import requests
import lxml
from xlwt import *
def main2(URL,pic,minim,maxim):
	HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763','Accept-Language': 'en-US, en;q=0.5'})

	# Making the HTTP Request
	webpage = requests.get(URL, headers=HEADERS)

	# Creating the Soup Object containing all data
	soup = BeautifulSoup(webpage.content, "lxml")

	# retrieving product title
	try:
		# Outer Tag Object
		title = soup.find("span",
						attrs={"id": 'productTitle'})

		# Inner NavigableString Object
		title_value = title.string

		# Title as a string value
		title_string = title_value.strip().replace(',', '')

	except AttributeError:
		title_string = "NA"
	print("product Title = ", title_string)

	# saving the title in the file

	# retrieving price
	try:
		price_parent = soup.find('span','a-price')
		price = price_parent.find('span','a-offscreen').text
        #price = soup.find("span", attrs={'id': 'priceblock_ourprice'}).string.strip().replace(',', '')
		# we are omitting unnecessary spaces
		# and commas form our string
	except AttributeError:
		price = "NA"
	print("Products price = ", price)

	# saving

	# retrieving product rating
	try:
		rating = soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip().replace(',', '')

	except AttributeError:

		try:
			rating = soup.find(
				"span", attrs={'class': 'a-icon-alt'}).string.strip().replace(',', '')
		except:
			rating = "NA"
	print("Overall rating = ", rating)


	try:
		review_count = soup.find(
			"span", attrs={'id': 'acrCustomerReviewText'}).string.strip().replace(',', '')

	except AttributeError:
		review_count = "NA"
	print("Total reviews = ", review_count)

	# print availablility status
	try:
		available = soup.find("div", attrs={'id': 'availability'})
		available = available.find("span").string.strip().replace(',', '')

	except AttributeError:
		available = "NA"
	print("Availability = ", available)
	biggerbrand = str.split(title_string)
	brand = biggerbrand[0]
	print("Brand = ", brand)

	# saving the availability and closing the line
	if minim == 'N/A':
		minim = price
	if maxim == 'N/A':
		maxim = price        
	result = [title_string,price,rating,review_count,available,URL,pic,brand,minim,maxim]
	return result
	# closing the file


