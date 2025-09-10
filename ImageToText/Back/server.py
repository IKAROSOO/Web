from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import base64
import io

app = Flask(__name__)
CORS(app)

@app.route('/image-processing', methods=["POST"])
def image_processing():
    data = request.get_json()

    if not data or 'imageData' not in data:
        return jsonify({"Error" : "No image data provided"}), 400
    
    base64_image_data = data['imageData']

    try:
        header, encoded = base64_image_data.split(",", 1)
        image_data = base64.b64decode(encoded)
        image = Image.open(io.BytesIO(image_data))

        # 이미지가 정상적으로 전달되는지 확인
        # image.show()

        print(f"Image received successfully: format={image.format}, size={image.size}")
    except Exception as e:
        print(f"Error processing image: {e}")
        return jsonify({"error": "Invalid image data"}), 400

    response_data = {
        'status' : "success",
        'message' : "Image received successfully!",
        "extracted_text" : "이곳에 Gemini가 추출한 텍스트가 들어갈 예정"
    }
    return jsonify(response_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
