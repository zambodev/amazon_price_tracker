#!/usr/bin/python
import requests
import sys
import json
from bs4 import BeautifulSoup


if __name__ == "__main__":

	with open(sys.argv[1], "r") as file:
		data = file.read()

	obj = json.loads(data)

	header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"}

	for chunk in obj:
		url = chunk['url']

		page = requests.get(url,headers=header)
		soup = BeautifulSoup(page.content, "html.parser")
		title = soup.find("span", {"id":"productTitle"})
		if title:
			title = title.get_text().lstrip()
		else:
			continue
		price = soup.find("span", {"class":"a-offscreen"}).get_text()

		price_list = chunk['price_list']
		min_price = None if not price_list else min(price_list)
		print("Object: {}\nBest price: {} Price: {}\n".format(title, min_price, price))

		if not price in price_list:
			price_list.append(price)
			chunk['price_list'] = price_list

	with open(sys.argv[1], "w") as file:
		json.dump(obj, file)
