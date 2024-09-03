from flask import Flask, request, send_file
import cv2
import easyocr
import numpy as np
from io import BytesIO
from PIL import Image

app = Flask(__name__)

@app.route('/upload/', methods=['POST'])
def upload_image():
    # Kiểm tra nếu file được gửi trong yêu cầu
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']

    # Đọc ảnh từ file upload
    img = Image.open(file.stream)
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    # Lấy màu nền từ góc trên bên trái của ảnh
    background_color = tuple(map(int, img[0, 0]))

    # Khởi tạo đối tượng đọc chữ
    reader = easyocr.Reader(['en'])
    text_ = reader.readtext(img)

    threshold = 0.25
    for t_, t in enumerate(text_):
        bbox, text, score = t

        if score > threshold:
            cv2.rectangle(img, tuple(map(int, bbox[0])), tuple(map(int, bbox[2])), background_color, -1)

    # Chuyển đổi ảnh thành định dạng JPEG
    _, img_encoded = cv2.imencode('.jpg', img)
    img_bytes = img_encoded.tobytes()

    return send_file(BytesIO(img_bytes), mimetype='image/jpeg')

@app.route('/hello/')
def hello():
    return "hello"
if __name__ == '__main__':
    app.run(debug=True)
