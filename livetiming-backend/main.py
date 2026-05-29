from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import time

app = FastAPI(title="Live Score Admin API")

# Cấu hình CORS để web tĩnh có thể gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()

class ScoreEvent(BaseModel):
    team: str
    score: str
    delay: int = 10  # Độ trễ mặc định 10 giây nếu Admin không truyền

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # Chế độ chờ: Client chỉ nhận chứ không gửi gì lên server (Keep-alive)
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/admin/score")
async def trigger_goal(event: ScoreEvent):
    """
    API dành cho Admin để báo sự kiện Ghi Bàn.
    Khi gọi API này, toàn bộ client đang kết nối WebSocket sẽ nhận được tỷ số mới.
    """
    payload = {
        "event_timestamp": time.time() * 1000,
        "team": event.team,
        "score": event.score,
        "delay": event.delay
    }
    await manager.broadcast(payload)
    return {"status": "success", "message": "Đã bắn sự kiện cập nhật tỷ số tới toàn bộ người xem!", "data": payload}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
