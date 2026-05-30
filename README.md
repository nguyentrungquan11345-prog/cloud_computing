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

## Các vấn đề hệ thống đã giải quyết

### 1. Giảm thiểu Độ trễ Video (Video Streaming Latency)
Vấn đề này phát sinh từ quá trình mã hóa, truyền tải mạng và xử lý trên cloud.
- **Giao thức Low-Latency**: Chuyển từ các giao thức truyền thống như HLS/DASH sang LL-HLS (Low-Latency HLS) hoặc WebRTC. WebRTC có thể đưa độ trễ từ mức hàng chục giây xuống dưới 1 giây (sub-second).
- **Tối ưu hóa Pipeline trên Cloud**: Để giảm thiểu thời gian xử lý khi luồng video từ camera được gửi lên cloud, thiết lập các dịch vụ đám mây chuyên dụng cho media (ví dụ như AWS Elemental MediaLive) để tăng tốc độ chuyển mã (transcoding) và đóng gói (packaging) video theo thời gian thực.

### 2. Khắc phục Giới hạn API (API Rate Limit & Quota Bottleneck)
Việc polling API liên tục không ổn định và dễ gây lỗi cập nhật dữ liệu.
- **Backend Trung gian (BFF - Backend For Frontend)**: Tránh việc để thiết bị của người dùng (client) gọi trực tiếp vào API thể thao. Xây dựng một server trung gian có nhiệm vụ gọi API theo chu kỳ được phép, sau đó lưu cache dữ liệu vào bộ nhớ tạm (ví dụ: Redis).
- **Kiến trúc Push qua WebSockets**: Từ server trung gian này, triển khai các framework xử lý bất đồng bộ tốc độ cao (như FastAPI) kết hợp với WebSockets để chủ động đẩy (push) dữ liệu điểm số mới nhất xuống hàng ngàn client cùng lúc, loại bỏ hoàn toàn việc tạo áp lực lên nhà cung cấp API.

### 3. Xử lý Mạng không ổn định (Network Instability)
Tình trạng mạng kém phía người xem gây rớt gói tin (packet loss), jitter và gián đoạn video.
- **Adaptive Bitrate Streaming (ABR)**: Hệ thống cloud tạo ra nhiều luồng video với các độ phân giải khác nhau (1080p, 720p, 480p). Video player ở phía client sẽ liên tục đo lường băng thông thực tế và tự động chuyển đổi (scale down/up) giữa các luồng này một cách mượt mà để tránh hiện tượng buffering.
- **Giao thức truyền tải chống lỗi**: Thay vì dùng RTMP, sử dụng giao thức SRT (Secure Reliable Transport) cho chặng đường đẩy stream từ sân vận động lên cloud. SRT có cơ chế phục hồi gói tin, xử lý packet loss và jitter tốt hơn rất nhiều.

### 4. Đồng bộ hóa Điểm số và Video (Score-Video Synchronization)
Điểm số cập nhật nhanh hơn video, gây ra tình trạng "spoil" kết quả trước khi người xem thấy sự kiện hiển thị trên màn hình.
- **Chèn Metadata (SEI) vào Video**: Chèn các mốc thời gian tuyệt đối (timestamp) vào chính luồng video thông qua chuẩn SEI (Supplemental Enhancement Information).
- **Bộ đệm thông minh phía Client**: Khi client nhận được dữ liệu bàn thắng qua luồng WebSocket, thay vì hiển thị lên UI ngay lập tức, ứng dụng sẽ đọc timestamp của sự kiện ghi bàn đó và đối chiếu với SEI metadata của khung hình video đang được chiếu. Điểm số sẽ được giữ trong một hàng đợi (queue) và chỉ được render ra màn hình khi video thực sự phát đến đúng thời điểm xảy ra sự kiện đó.
