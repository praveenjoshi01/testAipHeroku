"""
Author: praveenJoshi
Modified: Friday, 20th March 2020 2:44:13 pm [praveenJoshi]
"""

from flask import Flask, jsonify, g
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import pandas as pd
import re
import json

app = Flask(__name__)

@app.route("/statesstatus", methods=["GET"])
def states():
    response = requests.get('https://www.mohfw.gov.in/')
    if response.status_code != 200:
        print(f"{datetime.now()} : Server unresponsive!")
    text = response.text
    soup = BeautifulSoup(text, "lxml")
    table = soup.find(text="S. No.").find_parent("table")
    rows = table.find_all("tr")
    list_state = []
    for tr in rows:
        td = tr.find_all('td')
        row = [tr.text for tr in td]
        if len(row) != 0 and row[0].isdigit():
            list_state.append(row)

    new_df = pd.DataFrame(
        columns=['Sno', 'StateOrUt', 'TotalConfirmedCasesInIndia', 'TotalConfirmedCasesForeignNational', 'Cured',
                 'Death'], data=list_state)
    return new_df.to_json(orient='split')

@app.route("/countrystatus", methods=["GET"])
def overall():
    response = requests.get('https://www.mohfw.gov.in/')
    if response.status_code != 200:
        print(f"{datetime.now()} : Server unresponsive!")
    text = response.text
    soup = BeautifulSoup(text, "lxml")
    table = soup.find(text="S. No.").find_parent("table")
    rows = table.find_all("tr")
    confirmed = -1
    recovered = -1
    death = -1
    for tr in rows:
        td = tr.find_all('td')
        row = [tr.text for tr in td]
        if len(row) != 0 and not row[0].isdigit():
            if row[0] in ['Total number of confirmed cases in India']:
                print(row)
                confirmed = re.sub('[^0-9,.]', '', row[1])
                recovered = re.sub('[^0-9,.]', '', row[3])
                death = re.sub('[^0-9,.]', '', row[4])
    overall_status= {'confirmed':confirmed,'recovered':recovered,'death':death}
    overall_status_json = json.dumps(overall_status)
    return jsonify(overall_status_json)

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == "__main__":
    app.run(threaded=True, port=5000)