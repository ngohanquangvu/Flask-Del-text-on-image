from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
import cv2
import easyocr
import numpy as np
from io import BytesIO
from PIL import Image

app = FastAPI()

@app.post("/upload/")
def upload_image(file: UploadFile = File(...)):
    # Kiểm tra nếu file được gửi trong yêu cầu
    if not file:
        raise HTTPException(status_code=400, detail="No file part")

    # Đọc ảnh từ file upload
    contents = file.file.read()
    img = Image.open(BytesIO(contents))
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

    return StreamingResponse(BytesIO(img_bytes), media_type="image/jpeg")

@app.get("/hello/")
def hello():
    return {"message": "hello"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
