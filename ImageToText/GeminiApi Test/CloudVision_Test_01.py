import io
import os
import CloudVision_Test_00 as config
from google.cloud import vision

CONFIG_PATH = config.CONFIG_PATH
client = config.client
image_path = config.os.path.join(config.file_path, 'Test_Image_02.png')

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