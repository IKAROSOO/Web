import google.generativeai as genai
import json

# 해당 config.json의 파일경로는 컴퓨터에 따라 변해야한다.
CONFIG_PATH = 'Personal/Image/config.json'

# json파일을 읽어와서 API_KEY값을 뽑아내는 구문
with open(CONFIG_PATH, 'r') as f:
    try:
        data = json.load(f)
        API_KEY = data['API_KEY']
    except FileNotFoundError:
        print(f"Error : {CONFIG_PATH} can't Found!")
    except json.JSONDecodeError:
        print(f"Error : {CONFIG_PATH} isn't Correct JSON FILE!")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

answer = ""

