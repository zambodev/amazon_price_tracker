#!/usr/bin/python
import requests
import sys
import json
from bs4 import BeautifulSoup


if __name__ == "__main__":

	with open(sys.argv[1], "r") as file:
		data = file.read()

	obj = json.loads(data)

	for chunk in obj:
		url = chunk['url']

		page = requests.get(url,headers={"User-Agent":"Defined"})
		soup = BeautifulSoup(page.content, "html.parser")
		name = soup.find("span", {"id":"productTitle"}).get_text().lstrip()
		price = soup.find("span", {"class":"a-offscreen"}).get_text()

		price_list = chunk['price_list']
		min_price = None if not price_list else min(price_list)
		print("Object: {}\nBest price: {} Price: {}\n".format(name, min_price, price))

		if not price in price_list:
			price_list.append(price)
			chunk['price_list'] = price_list

	with open(sys.argv[1], "w") as file:
		json.dump(obj, file)
