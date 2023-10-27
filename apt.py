#!/usr/bin/env python3

import requests
import json
import time
import sys
import re
import os
from statistics import fmean
from bs4 import BeautifulSoup


def link(uri, label=None):
    if label is None: 
        label = uri
    parameters = ''

    escape_mask = '\033]8;{};{}\033\\{}\033]8;;\033\\'

    return escape_mask.format(parameters, uri, label)

if __name__ == "__main__":
    # Check if argument is present
    if len(sys.argv) == 1:
        print("Missing argument: apt.py <file>.json <title>:'<link>'")
        sys.exit()


    # Headless browser headers
    header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"}
	
    if "-i" in sys.argv:
        pid = os.fork()
        if pid != 0:
            print("Cild pid: " + str(pid))
    else:
        pid = 1

    if pid == 0:    # Child section
        while True:
            # Open json file
            with open(sys.argv[1], "r") as file:
                obj_list = json.loads(file.read())

            for obj in obj_list:

                title = obj['title']
                url = obj['url']

                try:
                    page = requests.get(url, headers=header, timeout=60)
                    if(page.status_code != 200): 
                        continue

                    soup = BeautifulSoup(page.content, "html.parser")

                    price_text = soup.find("span", {"class":"a-offscreen"})
                    if(not price_text):
                        continue

                    price = float(re.findall(r"[-+]?(?:\d*\.*\d+)", price_text.get_text().replace(',','.'))[0])
                    sign = soup.find("span", {"class":"a-price-symbol"}).get_text()

                    price_list_str = obj['price_list']
                    price_list = [float(i.replace(',','.')) for i in price_list_str]


                    if not str(price) in price_list_str:
                        price_list_str.append(str(price))
                        obj['price_list'] = price_list_str

                    with open(sys.argv[1], "w") as file:
                        file.write(json.dumps(obj_list, indent=3))

                except:
                    continue

            time.sleep(3600.0)
    else:           # Parent process
                    # Open json file
        with open(sys.argv[1], "r") as file:
            obj_list = json.loads(file.read())

        for obj in obj_list:

            title = obj['title']
            url = obj['url']

            price_list_str = obj['price_list']
            price_list = [float(i.replace(',','.')) for i in price_list_str]

            min_price = None if not price_list else format(float(min(price_list)), '.2f')
            avg_price = None if not price_list else format(float(fmean(price_list)), '.2f')
            max_price = None if not price_list else format(float(max(price_list)), '.2f')
            price = format(float(price_list[-1]), '.2f')

            print(link(url, title))
            print(f"Range: {min_price} - {max_price}")
            print(f"Avg: {avg_price}")
            print(f"Latest: {price}")

            if not str(price) in price_list_str:
                price_list_str.append(str(price))
                obj['price_list'] = price_list_str

            print("--------------------------------")
    