# Live Sports Streaming Platform Demo

## Hướng dẫn cài đặt và chạy hệ thống

### Bước 1: Khởi động Nginx-RTMP Server
Đảm bảo bạn đã cài đặt Docker và Docker Compose. Chạy lệnh sau tại thư mục gốc của dự án:
```bash
docker compose up -d
```
*(Nếu cổng 1935 bị trùng với phần mềm khác trên máy, hãy tắt phần mềm đó hoặc đổi cổng trong file docker-compose.yml)*

### Bước 2: Khởi động Backend (Websocket)
Di chuyển vào thư mục backend và chạy server FastAPI (cần cài đặt `uv` hoặc `pip`):
```bash
cd livetiming-backend
uv run uvicorn main:app --reload --port 8000
```

### Bước 3: Đẩy luồng Live Stream bằng OBS
Mở phần mềm OBS Studio, thiết lập cấu hình Stream:
- **Service:** Custom
- **Server:** `rtmp://127.0.0.1/live`
- **Stream Key:** `test`
Bấm **Start Streaming**.

### Bước 4: Mở giao diện xem Live
- Sử dụng trình duyệt mở trực tiếp file `index.html`.
- Hoặc để tối ưu nhất, hãy chạy một máy chủ tĩnh:
```bash
python3 -m http.server 3000
```
Sau đó truy cập `http://localhost:3000` trên trình duyệt để trải nghiệm.
