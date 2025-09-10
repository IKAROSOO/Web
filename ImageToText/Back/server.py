from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import base64
import io

app = Flask(__name__)
CORS(app)

app.run(port=5000, debug=True)
@app.route('/image-processing', methods=["POST"])

def image_processing():
    answer = 0
    