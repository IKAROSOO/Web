from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
from threading import Timer
import pandas as pd
import webbrowser
import datetime
import requests
import json
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
url_path = os.path.join(current_dir, 'urls.json')
env_path = os.path.join(current_dir, 'apikey.env')

app = Flask(__name__,
            template_folder=os.path.join(current_dir, "../Web/HTML"),
            static_folder=os.path.join(current_dir, "../Web"),
            static_url_path='')

# ----- env파일에서 API KEY를 획득 -----
load_dotenv(dotenv_path=env_path)
FRED_API_KEY = os.getenv("FRED_API")
# ----------

# ----- API KEY를 찾지 못하면 즉시 프로그램 종료 -----
if FRED_API_KEY is None:
    print("Can't Find API KEY")
    sys.exit(1)
# ----------

# ----- Json을 불러와 URL데이터를 추출하는 과정 -----
try:
    with open(url_path, 'r', encoding='utf-8') as f:
        URL_DATA = json.load(f)
# ----------

# ----- Json파일을 찾지 못하면 즉시 프로그램 종료 -----
except FileNotFoundError:
    print("Can't Fint Json File")
    print("ShutDown the Program")
    sys.exit(1)
# ----------

indicator_list = {
    "exchange-rate": "DEXKOUS",
    "rcv": "RBKRBIS",
    "br": "DFF",
    "reer": "REEROKUS"
}

# def ExchangeRate(api_key, url_data, series_id, start_date):
#     URL = url_data['FRED_Exchange']
#     params = {
#         'series_id': series_id,
#         'api_key': api_key,
#         'file_type': 'json',
#         'observation_start': start_date
#     }

#     response = requests.get(URL, params=params)

#     # ----- 응답에 성공하여 파일을 받아온 상황 -----
#     if response.status_code == 200:
#         exchange_data = response.json()
#         df = pd.DataFrame(exchange_data['observations'])[['date', 'value']]
#         df['value'] = pd.to_numeric(df['value'], errors='coerce')
#         df['date'] = pd.to_datetime(df['date'])
#         df.set_index('date', inplace=True)

#         return df
#     # ----------
    
#     # ----- 응답에 실패한 경우 -----
#     else:
#         print(f"Error: {response.status_code}")
#         print(f"Error details: {response.text}")
#         return None
#     # ----------

def getData(api_key, url_data, series_id, start_date):
    URL = url_data['FRED_OBSERVATIONS_ENDPOINT']
    params = {
        'series_id': series_id,
        'api_key': api_key,
        'file_type': 'json',
        'observation_start': start_date
    }

    response = requests.get(URL, params=params)

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data['observations'])[['date', 'value']]

        df["value"] = pd.to_numeric(df["value"], errors='coerce')
        
        df = df.replace({pd.NA: None}).where(pd.notnull(df), None)
        df = df.astype(object).where(df.notnull(), None)

        return df.to_dict(orient='records'  )
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
def data_Request():
    indicator = request.args.get('indicator')
    period = request.args.get('period')
    
    today = datetime.date.today()
    if period.isdigit():
        past = today - datetime.timedelta(days=(365*int(period)))

    if not indicator or not period:
        return jsonify({"error": "missing parameter"}), 400

    print(f"수신된 요청 -> 카드ID: {indicator}, 기간 :{period}")

    data = getData(FRED_API_KEY, URL_DATA, indicator_list[indicator], past)

    result = {
        "indicator": indicator,
        "frequency": "Daily",
        "data": data
    }

    return jsonify(result)

if __name__ == '__main__':
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        Timer(1.5, OpenBrowser).start()

    app.run(debug=True, port=5050)