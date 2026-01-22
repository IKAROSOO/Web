from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import datetime
import requests
import json
import sys
import os

def set_korean_font():
    font_name = None
    if sys.platform == "darwin": # Mac
        font_name = 'AppleGothic'
    elif sys.platform == "win32": # Windows
        font_name = 'Malgun Gothic'
    else: # Linux 등 다른 OS
        # 나눔고딕이 설치되어 있다면 사용
        if 'NanumGothic' in [f.name for f in fm.fontManager.ttflist]:
            font_name = 'NanumGothic'
        else:
            print("Linux 환경, 나눔고딕 폰트가 없으면 한글이 깨질 수 있습니다.")
            print("sudo apt-get install fonts-nanum* 명령어로 설치 가능합니다.")
            font_name = 'DejaVu Sans' # 기본 영어 폰트로 대체

    if font_name and font_name in [f.name for f in fm.fontManager.ttflist]:
        plt.rcParams['font.family'] = font_name
        plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지
    else:
        print(f"경고: {font_name} 폰트를 찾을 수 없습니다. 기본 폰트로 표시됩니다.")
        print("설치된 폰트 목록을 확인하고 직접 설정할 수도 있습니다.")
        # 예시: for f in fm.fontManager.ttflist: print(f.name)
        
set_korean_font()

def plotExchangeRate(df, title="환율 추이", ylabel="환율 (원)"):
    plt.figure(figsize=(12, 6))

    if isinstance(df, pd.DataFrame):
        for column in df.columns:
            plt.plot(df.index, df[column], label=column)
    else:
        plt.plot(df.index, df.values, label=df.name if df.name else "환율")

    plt.title(title, fontsize=16)
    plt.xlabel("날짜", fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7) # 그리드 표시
    plt.legend(fontsize=10) # 범례 표시
    plt.tight_layout() # 그래프 레이아웃 자동 조정
    # plt.savefig(filename) # 파일로 저장
    plt.show() # 화면에 표시

def ExchangeRate(api_key, data, series_id, start_date):
    URL = data['FRED_Exchange']
    params = {
        'series_id': series_id,
        'api_key': api_key,
        'file_type': 'json',
        'observation_start': start_date,
    }

    response = requests.get(URL, params=params)

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data['observations'])[['date', 'value']]
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        return df
    else:
        print(f"Error: {response.status_code}")
        print(f"Error details: {response.text}")
        return None

def main():
    today = datetime.date.today()
    past = today - datetime.timedelta(days=(365*15))

    currnet_dir = os.path.dirname(os.path.abspath(__file__))
    url_path = os.path.join(currnet_dir, 'urls.json')
    env_path = os.path.join(currnet_dir, 'apikey.env')
    
    load_dotenv(dotenv_path=env_path)

    FRED_API_KEY = os.getenv("FRED_API")
    if FRED_API_KEY is None:
        print("FRED API KEY를 찾을 수 없습니다.")
        sys.exit(1)

    try:
        # Json에서 URL을 불러오는 try-except문
        with open(url_path, 'r', encoding='utf-8') as f:
            URL = json.load(f)
    except FileNotFoundError:
        # Json에서 파일을 불러오지 못할 경우, 바로 프로그램을 종료하게 한다.
        print('Json파일을 찾을 수 없습니다.')
        print('프로그램을 종료합니다.')
        sys.exit(1)

    krw_usd = ExchangeRate(FRED_API_KEY, URL, 'DEXKOUS', past)

    if krw_usd is not None:
        print("데이터 로드 성공")

        plotExchangeRate(krw_usd.dropna(),
                         title="원/달러 환율 추이 (15년)", 
                         ylabel="환율 (원/달러)")
    else:
        print("원/달러 환율 데이터를 가져오지 못했습니다.")

if __name__ == '__main__':
    main()