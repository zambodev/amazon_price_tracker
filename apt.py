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
		limit = len(name) if len(name) < 60 else 60
		old_price = chunk['old_price']
		print("Object: {}\nOld price: {} Price: {}\n".format(name, old_price, price))

		chunk['old_price'] = price
		chunk['price'] = old_price

	with open(sys.argv[1], "w") as file:
		json.dump(obj, file)
