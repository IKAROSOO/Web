from PIL import Image
import Gemini_Test_00 as config
import google.generativeai as genai

'''
이미지에서 영문 텍스트를 추출하는 것이 가능한지 실증하는 코드
하지만 Gemini는 대화형 AI이기 때문에 Gemini의 자체 답변도 포함되어 있음
'''

genai.configure(api_key=config.API_KEY)
model = config.model

text_prompt = "I want yo to extract the texts in this Image"

image_path = config.os.path.join(config.file_path, 'Test_Image_02.png')
img = Image.open(image_path)

# img.show()

# prompt를 작성할 때는 Text, Img 순서로 넣는 것이 권장된다.
prompt = [
    text_prompt,
    img
]

try:
    print("Gemini is try to Answer...")
    response = model.generate_content(prompt)

    print("---Gemini's Answer---")
    print(response.text)
except Exception as e:
    print(f"Error : {e}")