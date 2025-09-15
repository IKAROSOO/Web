import io
import os
from google.cloud import vision

file_path = os.path.dirname(os.path.abspath(__file__))
script_path = os.path.dirname(file_path)
image_path = os.path.join(file_path, 'Test_Image_02.png')
CONFIG_PATH = os.path.join(script_path, 'CloudVision_config.json')

client = vision.ImageAnnotatorClient.from_service_account_file(CONFIG_PATH)

def main():
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    print('감지된 텍스트 : ')
    if texts:
        print(texts[0].description)
    else:
        print('텍스트를 감지하지 못했습니다.')

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
            response.error.message))

if __name__ == '__main__':
    main()