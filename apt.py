#!/usr/bin/python
import requests
import sys
import json
import statistics
from bs4 import BeautifulSoup


if __name__ == "__main__":

    with open(sys.argv[1], "r") as file:
        data = file.read()

    obj = json.loads(data)

    if len(sys.argv) > 2:
        for link in sys.argv[2:]:
            obj.append({"url":link,"price_list":[]})

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
        price = soup.find("span", {"class":"a-offscreen"}).get_text().replace(',','.')
        sign = price[-1]

        price_list_str = chunk['price_list']
        price_list = [float(i[:-1].replace(',','.')) for i in price_list_str]

        min_price = None if not price_list else min(price_list)
        avg_price = None if not price_list else statistics.fmean(price_list)
        max_price = None if not price_list else max(price_list)

        print("Object: {}\nWorst price: {}{} Avg price: {}{} Best price: {}{} Latest price: {}\n".format(title, max_price, sign, avg_price, sign, min_price, sign, price))
    
        if not price in price_list:
            price_list_str.append(price)
            chunk['price_list'] = price_list_str

    with open(sys.argv[1], "w") as file:
        file.write(json.dumps(obj, indent=4))

