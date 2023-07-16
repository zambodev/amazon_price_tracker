#!/usr/bin/python3

import requests
import sys
import json
import re
from statistics import fmean
from bs4 import BeautifulSoup


if __name__ == "__main__":

    if len(sys.argv) == 1:
        print("Missing argument: apt.py <file>.json <title>:'<link>'")
        sys.exit()

    with open(sys.argv[1], "r") as file:
        obj = json.loads(file.read())

    if len(sys.argv) > 2:
        for link in sys.argv[2:]:
            linksplit = link.split(":", 1)
            obj.append({"title":linksplit[0],"url":linksplit[1],"price_list":[]})

    header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"}

    for chunk in obj:
        url = chunk['url']

        page = requests.get(url, headers=header, timeout=60)
        if(page.status_code != 200): 
            continue
        
        soup = BeautifulSoup(page.content, "html.parser")

        price = re.findall(r"[-+]?(?:\d*\.*\d+)", soup.find("span", {"class":"a-offscreen"}).get_text().replace(',','.'))[0]
        sign = soup.find("span", {"class":"a-price-symbol"}).get_text()

        price_list_str = chunk['price_list']
        price_list = [float(i[:-1].replace(',','.')) for i in price_list_str]

        min_price = None if not price_list else min(price_list)
        avg_price = None if not price_list else fmean(price_list)
        max_price = None if not price_list else max(price_list)

        print(f"Object: {chunk['title']}")
        print(f"Range: {min_price}{sign} - {max_price}{sign}")
        print(f"Avg: {avg_price}{sign}")
        print(f"Latest: {price}{sign}")
        print("--------------------------------")
    
        if not price in price_list:
            price_list_str.append(price)
            chunk['price_list'] = price_list_str

    with open(sys.argv[1], "w") as file:
        file.write(json.dumps(obj, indent=4))

