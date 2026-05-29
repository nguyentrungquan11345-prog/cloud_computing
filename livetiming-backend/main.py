from fastapi import FastAPI, WebSocket
import uvicorn
import asyncio
import time

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Gửi dữ liệu giả lập (mock event) mỗi 5 giây
            await asyncio.sleep(5)
            await websocket.send_json({
                "event_timestamp": time.time() * 1000,
                "team": "Team Đỏ",
                "score": "1-0"
            })
    except Exception as e:
        print("Client disconnected:", e)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
