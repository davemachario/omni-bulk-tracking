from operator import index
from unicodedata import name
from flask import Flask, render_template, request, url_for, redirect
from __main__ import *
from deta import Deta

deta= Deta('c0d9yft4_M9BzX2P12KWUjbqoZ3F2YSaYs9AnaMsU')
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form["name"]
        return redirect(url_for('result', name=name))
    return render_template('index.html')


@app.route("/result", methods=['GET', 'POST'])
def result():
    name = request.form['name']
    print(type(name))
    ## Input Connotes from home
    connotes = [str(x) for x in name.splitlines()]
    def bulk_track(connotes):

        ## Process Connote to be URL
        url = []
        x = 0

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
        from tabulate import tabulate

        pd.set_option('display.max_colwidth', None)

        #scrape elements
        i = 0
        df = []
        tracking_number = []
        latest_date = []
        update = []
        location = []
        carrier = []

        while i < len(url):
            response = requests.get(url[i])
            soup = BeautifulSoup(response.content, "html.parser")

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

            tracking_number.append(data[0])
            latest_date.append(date.to_string(index=False))
            update.append(df[i]['Activity'].iloc[-4:-3].to_string(index=False))
            location.append(df[i]['Location'].iloc[-4:-3].to_string(index=False))
            carrier.append(df[i]['Carrier'].iloc[-4:-3].to_string(index=False))

            i+=1

        return tracking_number, latest_date, update, location, carrier


    return render_template("result.html", len = len(connotes), name=bulk_track(connotes))


if __name__ == "__main__":
    app.run()
