from unicodedata import name
from flask import Flask, render_template, request, url_for, redirect
from __main__ import *

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form["name"]
        return redirect(url_for('result', name=name))
    return render_template('home.html')


@app.route("/result", methods=['GET', 'POST'])
def result():
    name = request.form.get('name')

    def bulk_track(name):

        ## Input Connotes from home
        connotes = [str(x) for x in name.split()]

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

        pd.set_option('display.max_colwidth', None)

        #scrape elements
        i = 0
        df = []
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
            
            # Printing end result
            print(data[0], "\n",
                "Latest date: ", date.to_string(index=False), "\n" ,
                "Latest update: ", df[i]['Activity'].iloc[-4:-3].to_string(index=False), "\n",
                "Last Location", df[i]['Location'].iloc[-4:-3].to_string(index=False), "\n",
                "Carrier:", df[i]['Carrier'].iloc[-4:-3].to_string(index=False), "\n")
            
            # return "all executed well"

            i+=1

    return render_template("result.html", name=bulk_track(name))


if __name__ == "__main__":
    app.run(debug=True)