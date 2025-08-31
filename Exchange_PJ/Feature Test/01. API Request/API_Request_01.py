'''
요청하는 API주소를 cmd창에 띄우는 것이 목적인 코드

휴장일일 경우에는 json의 데이터가 "[]"로만 이루어졌음.

다른 코드에서 import할 때 url주소가 2번 나오지 않게 설정
'''

from datetime import datetime, timedelta
import json
import requests
import os

API_URL = "https://oapi.koreaexim.go.kr/site/program/financial/exchangeJSON"

def APIrequest(date_str, authKey):
    payload = {
        'authkey': authKey,
        'searchdate': date_str,
        'data': "AP01"
    }

    try:
        response = requests.get(API_URL, params=payload)

        print("요청 API 주소 : ", response.url)

        if response.status_code == 200:
            data = response.json()
            return data if data else None

    except requests.exceptions.RequestException as e:
        print(f"Error Occurred : {e}")
        return

today = datetime.today()
today_str = today.strftime("%Y%m%d")

base_dir = os.path.dirname(__file__)
config_path = os.path.join(base_dir, '../../Server/config.json')

with open(config_path, 'r') as f:
    config = json.load(f)

AUTH_KEY = config['AuthKey']

if __name__ == "__main__":
    APIrequest(today_str, AUTH_KEY)