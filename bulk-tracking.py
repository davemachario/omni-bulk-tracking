## Input Connotes
connotes = [str(x) for x in input("Enter your connotes here: \n").splitlines()]
# print("\nTotal connotes inputted: ", f"{len(connotes)} connotes")

## Process Connote to be URL
url = []
x = 0
# print(len(connotes))
while x < len(connotes):
    url.append(f"http://track.omniparcel.com/?id="+connotes[x])
    x+=1

## Accesss URL and scrape the data

from bs4 import BeautifulSoup
import requests
import pprint
import re
import pyperclip
import pandas as pd
import math

pd.set_option('display.max_colwidth', None)
#scrape elements
i = 0
df = []
while i < len(url):
    response = requests.get(url[i])
    soup = BeautifulSoup(response.content, "html.parser")

#     print(soup.prettify())
    table = soup.find_all('table')
    df.append(pd.read_html(str(table))[0])
    
    # Parsing date
    date = df[i]['Date/Time'].iloc[-5:-4]
    if date.str.match(pat = '(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)').any() == 0:
        k = 0
        while date.str.match(pat = '(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)').any() == 0:
            k+=1
            date = df[i]['Date/Time'].iloc[-5-k:-4-k]
    else:
        date = date
    
    
    selector = 'div.col-xs-12 > h3'

    # find elements that contain the data we want
    found = soup.select(selector)

    # Extract data from the found elements
    data = [x.text.split(';')[-1].strip() for x in found]

    for x in data:
        tracking = x
    
    # Printing end result
    print(data[0], "\n",
          "Latest date: ", date.to_string(index=False), "\n" ,
          "Latest update: ", df[i]['Activity'].iloc[-4:-3].to_string(index=False), "\n",
          "Last Location", df[i]['Location'].iloc[-4:-3].to_string(index=False), "\n",
          "Carrier:", df[i]['Carrier'].iloc[-4:-3].to_string(index=False), "\n")
    
    i+=1