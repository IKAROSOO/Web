from PIL import Image
import google.generativeai as genai
import Gemini_Test_00 as config
import json

'''
이미지에서 영문 텍스트를 추출하는 것은 동일하지만,
받아온 Response에서 최대한 정형화된 텍스트 추출을 하는 것이 목표
'''

genai.configure(api_key=config.API_KEY)
model = config.model

# 영문으로 질문하여 최대한 토큰 사용량을 줄이는 것이 목표 
text_prompt = '''
Your task is to act as an Optical Character Recognition (OCR) engine.
Extract all text from the provided image.
Your response MUST be a valid JSON object.
The JSON object should have a single key named "extracted_text".
The value of this key should be a string containing all the text found in the image.
Do not include any explanations, introductory text, or markdown formatting outside of the JSON object.

Example response:
{
  "extracted_text": "This is the text from the image."
}
'''

image_path = config.os.path.join(config.file_path, 'Test_Image_02.png')
img = Image.open(image_path)

prompts = [
    text_prompt,
    img
]

try:
    print("Gemini try to Answer...")
    response = model.generate_content(prompts)

    print("---Gemini's Answer---")
    # print(response.text)

    try:
        clean_response = response.text.strip().replace('```json', '').replace('```', '')
        data = json.loads(clean_response)
        extracted_text = data['extracted_text']

        print("\n---Successfully Extracted Text---\n")
        print(extracted_text)
    except json.JSONDecodeError as e:
        print(f"\nError parsing JSON or finding key : {e}")
except Exception as e:
    print(f"Error : {e}")