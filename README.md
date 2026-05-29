# Live Sports Streaming Platform Demo

Đây là một dự án mô phỏng hệ thống Live Streaming Thể thao (tương tự các trang trực tiếp bóng đá), bao gồm các thành phần:

1. **Nginx-RTMP Server (Docker):** 
   - Nhận luồng RTMP từ phần mềm OBS Studio.
   - Tự động chuyển đổi luồng RTMP sang định dạng HLS (HTTP Live Streaming).
   - Phục vụ file HLS qua cổng 8080 với cấu hình CORS đầy đủ để trình duyệt web có thể truy cập.

2. **Giao diện Web (Frontend):**
   - File `index.html` được thiết kế hiện đại, responsive, mô phỏng bố cục của các trang xem bóng đá trực tuyến.
   - Tích hợp thư viện `hls.js` để hỗ trợ phát luồng `.m3u8` ngay trên trình duyệt (bao gồm cả Chrome, Firefox, Edge).
   - Tích hợp kết nối WebSocket để hiển thị tỷ số và thông báo theo thời gian thực.

3. **FastAPI Server (Backend):**
   - Mã nguồn nằm trong thư mục `livetiming-backend`.
   - Chạy một máy chủ WebSocket ở cổng 8000 để mô phỏng việc đẩy dữ liệu tỷ số, sự kiện trận đấu (bàn thắng, thẻ phạt...) xuống trình duyệt liên tục.

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
