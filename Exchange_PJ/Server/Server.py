from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import json
import requests
import os

app = Flask(__name__)
CORS(app)

API_URL = "https://oapi.koreaexim.go.kr/site/program/financial/exchangeJSON"

def FetchExchangeRate(date_str, authkey):
    payload = {
        'authkey': authkey,
        'searchdate': date_str,
        'data': "AP01"
    }

    try:
        response = requests.get(API_URL, params=payload)

        print("요청 API주소 : ", response.url)

        if response.status_code == 200:
            data = response.json()
            return data if data else None
        return None
    except requests.exceptions.RequestException:
        return None

@app.route("/api/exchange-rate", methods=['GET'])
def SendData():
    base_dir = os.path.dirname(__path__)
    config_path = os.path.join(base_dir, 'config.json')

    with open(config_path, 'r') as f:
        config = json.load(f)
    AUTH_KEY = config['AuthKey']

    today = datetime.now()
    today_str = today.strftime("%Y%m%d")
    today_rate = FetchExchangeRate(today_str, AUTH_KEY)

    if not today_rate:
        return jsonify({"Error": "오늘의 환율 데이터를 가져올 수 없습니다."}), 500





# def getChangingData():
#     base_dir = os.path.dirname(__file__)
#     config_path = os.path.join(base_dir, 'config.json')

#     with open(config_path, "r") as f:
#         config = json.load(f)
#     AUTH_KEY = config['AuthKey']

#     today = datetime.now()
#     today_str = today.strftime("%Y%m%d")
#     today_rate = FetchExchangeRate(today_str, AUTH_KEY)

#     if not today_rate:
#         return jsonify({"Error": "오늘의 환율 데이터를 가져올 수 없습니다."}), 500
    
#     previous_rate = None

#     for day in range(1, 8):
#         previous = today-timedelta(days=day)
#         previous_str = previous.strftime("%Y%m%d")
#         previous_rate = FetchExchangeRate(previous_str, AUTH_KEY)

#         if previous_rate:
#             break
#     if not previous_rate:
#         return jsonify({"Error": "직전 영업일의 환율 데이터를 가져올 수 없습니다."}), 500
    
#     today_dict = {rate['cur_unit']: rate for rate in today_rate}
#     previous_dict = {rate['cur_unit']: rate for rate in previous_rate}

#     results = list()

#     for currency, today_data in today_dict.items():
#         if currency in previous_dict:
#             previous_data = previous_dict[currency]

#             today_price = float(today_data['tts'].replace(',', ''))
#             previous_price = float(previous_data['tts'].replace(',', ''))

#             change = round(today_price-previous_price, 2)

#             if change > 0:
#                 direction = "up"
#             elif change < 0:
#                 direction = 'down'
#             else:
#                 direction = 'same'

#             results.append({
#                 "currency_code": currency,
#                 "currency_name": today_data['cur_nm'],
#                 "buy_price": today_data['ttb'],
#                 "sell_price": today_data['tts'],
#                 "change": change,
#                 "direction": direction
#             })
    
#     return jsonify(results)    

if __name__ == "__main__":
    app.run(debug=True)