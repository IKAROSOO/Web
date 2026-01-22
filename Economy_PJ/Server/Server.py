from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
from threading import Timer
import pandas as pd
import webbrowser
import datetime
import requests
import json
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
url_path = os.path.join(current_dir, 'urls.json')
env_path = os.path.join(current_dir, 'apikey.env')

app = Flask(__name__,
            template_folder=os.path.join(current_dir, "../Web/HTML"),
            static_folder=os.path.join(current_dir, "../Web"),
            static_url_path='')

load_dotenv(dotenv_path=env_path)
FRED_API_KEY = os.getenv("FRED_API")

indicator_list = {
    "exchange-rate": "DEXKOUS",
    "rcv": "RBKRBIS",
    "br": "DFF",
    "reer": "REEROKUS"
}

period_list = {
    '1y': 1,
    '5y': 5,
    '10y': 10,
    'custom': -1
}

if FRED_API_KEY is None:
    print("Can't Fine API KEY")
    sys.exit(1)

try:
    with open(url_path, 'r', encoding='utf-8') as f:
        URL_DATA = json.load(f)
except FileNotFoundError:
    print("Can't Fine Json File")
    print("ShutDown the Program")
    sys.exit(1)

def ExchangeRate(api_key, url_data, series_id, start_date, end_date):
    if end_date is None:
        end_date = datetime.date.today().strftime("%Y-%m-%d")

    URL = url_data['FRED_OBSERVATIONS_ENDPOINT']
    params = {
        'series_id': series_id,
        'api_key': api_key,
        'file_type': 'json',
        'observation_start': start_date,
        'observation_end': end_date
    }

    response = requests.get(URL, params=params)

    if response.status_code == 200:
        exchange_data = response.json()
        df = pd.DataFrame(exchange_data['observations'])[['date', 'value']]

        df['value'] = pd.to_numeric(df['value'], errors='coerce')

        df = df.replace({pd.NA: None}).where(pd.notnull(df), None)
        df = df.astype(object).where(df.notnull(), None)

        return df.to_dict(orient='records')
    else:
        print(f"Error: {response.status_code}")
        print(f"Error details: {response.text}")
        return None

def OpenBrowser():
    webbrowser.open_new('http://127.0.0.1:5050/')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def data_request():
    indicator = request.args.get('indicator')
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')

    print(start_date, end_date)

    today = datetime.date.today()
    if start_date in period_list:
        start_date = today - datetime.timedelta(days=(365*(period_list[start_date])))
        end_date = None
    # else:
    #     start = datetime.date.strftime(start_date, "%Y-%m-%d")
    #     end = datetime.date.strftime(end_date, "%Y-%m-%d")
    
    if not indicator or not start_date:
        return jsonify({"error": "missing parameter"}), 400
    
    print(f"수신된 요청 -> 카드 ID: {indicator}, 기간: {start_date}")

    data = ExchangeRate(FRED_API_KEY, URL_DATA, indicator_list[indicator], start_date, end_date)
    result = {
        "indicator": indicator,
        'frequency': "Daily",
        'data': data
    }

    return jsonify(result)

if __name__ == '__main__':
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        Timer(1.5, OpenBrowser).start()

    app.run(debug=True, port=5050)