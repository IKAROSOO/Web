import google.generativeai as genai
import json
import os

# 해당 config.json의 파일경로는 컴퓨터에 따라 변해야한다.
# os 라이브러리를 활용해 항상 config.json의 절대경로를 파악
file_path = os.path.dirname(os.path.abspath(__file__))
script_path = os.path.dirname(file_path)
CONFIG_PATH = os.path.join(script_path, 'config.json')

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

def main():
    prompt = "This is API Test. If you recognize this, say something"

    try:
        response = model.generate_content(prompt)

        print("---Gemini's Answer---")
        print(response.text)
    except Exception as e:
        print(f"Error : {e}")

if __name__ == "__main__":
    main()