from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from threading import Timer
import pandas as pd
import webbrowser
import datetime
import requests
import json
import sys
import os

def get_app_root():
    '''
    개발 / 테스트 / pyinstaller / onefile 모두 대응 가능한 경로를 설정하는 함수
    '''

    # Pyinstaller onefile
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS

    # 개발 / 테스트    
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

APP_ROOT = get_app_root()

url_path = os.path.join(APP_ROOT, "Server", "urls.json")
env_path = os.path.join(APP_ROOT, "Server", 'apikey.env')

WEB_DIR = os.path.join(APP_ROOT, "Web")
HTML_DIR = os.path.join(WEB_DIR, "HTML")

app = Flask(__name__)
CORS(app)

load_dotenv(dotenv_path=env_path)
FRED_API_KEY = os.getenv("FRED_API")

# print(f"\n\n{FRED_API_KEY}\n\n")

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

# print(f'\n\n{URL_DATA}\n\n')

# 요청받은 국가의 일간 환율데이터를 API요청 후 반환하는 함수
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

# 요청할 수 있는 일간 환율데이터의 series_id 목록을 반환하는 함수
def ExchangeRate_series(api_key, url_data):
    url = url_data['FRED_CurrencyList']

    params = {
        "search_text": "exchange rate",
        "api_key": api_key,
        "file_type": "json",
        "filter_variable": "frequency",
        "filter_value": "Daily",  # 무조건 일간 데이터만 필터링
        "order_by": "popularity",
        "sort_order": "desc",
        "limit": 1000,
        "offset": 0
    }

    result = []

    try:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(response.text)
            return None

        data = response.json()
        seriess = data.get("seriess", [])

        for series in seriess:
            series_id = series.get("id", "")

            # USD 기준 일간 환율만
            if (
                series_id.startswith("DEX")
                and series_id.endswith("US")
                and len(series_id) in (7, 8)
            ):
                currency_code = series_id[3:-2]  # KO, JP, CH ...

                result.append({
                    "currency_fred": currency_code,
                    "series_id": series_id,
                })

        return result

    except Exception as e:
        print(e)

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

@app.route('/api/exchange_series')
def exchange_series():
    series_info = ExchangeRate_series(FRED_API_KEY, URL_DATA)

    print("환율 데이터 시리즈 정보 요청됨")

    if(series_info):
        print(f"환율 시리즈 개수: {len(series_info)}")
        # print(series_info)
    else:
        print("환율 시리즈 정보를 가져오지 못함")
    
    if series_info:
        return jsonify(series_info)
    else:
        return jsonify({"error": "Could not fetch exchange rate series"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5050)