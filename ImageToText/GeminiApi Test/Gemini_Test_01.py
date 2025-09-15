from PIL import Image
import Gemini_Test_00 as config
import google.generativeai as genai

'''
이미지와 텍스트를 한번에 묶어서 API에 질문하는 것을 실증하는 코드
'''

genai.configure(api_key=config.API_KEY)
model = config.model

image_path = config.os.path.join(config.file_path, 'Test_Image_01.jpg')
img = Image.open(image_path)

# 이미지가 제대로 나오는지 확인
# image.show()

text_prompt = "I want to know what mobile game this character come from"

try:
    print(f"Opening Image File : {image_path}")
    
    prompts = [
        text_prompt,
        img
    ]

    print("Gemini is try to answer...")
    response = model.generate_content(prompts)

    print("\nGemini's Answer\n")
    print(response.text)

except Exception as e:
    print(f"Error : {e}")