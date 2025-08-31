'''
불러온 데이터가 "[]"로 이루어져 있어,
데이터가 있는 날까지 거슬러 올라가도록 하는 코드
'''

import API_Request_01 as API

today = API.today_str

AUTH_KEY = API.AUTH_KEY

data = API.APIrequest(today, AUTH_KEY)

while not data:
    print(f"현재 날짜 {today}는 데이터가 없습니다.")
    print("작일 데이터를 확인합니다.")

    date_str = API.datetime.strptime(today, "%Y%m%d")
    date = date_str - API.timedelta(days=1)
    today = date.strftime("%Y%m%d")

    data = API.APIrequest(today, AUTH_KEY)

print(data)