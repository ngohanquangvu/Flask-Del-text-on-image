# Sử dụng image chính thức của Python
FROM python:3.8-slim

# Cài đặt các gói cần thiết
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0

# Tạo thư mục làm việc
WORKDIR /app

# Sao chép các file yêu cầu vào thư mục làm việc
COPY requirements.txt .

# Cài đặt các thư viện Python
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn vào thư mục làm việc
COPY . .

# Chạy ứng dụng FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
