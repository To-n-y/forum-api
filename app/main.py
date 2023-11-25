from app.handlers import router
from fastapi import FastAPI, WebSocket
from scripts.create_db import main as create_db
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocketDisconnect


def create_app():
    create_db()
    application = FastAPI()
    application.include_router(router)
    return application


app = create_app()

chat_rooms = {}


@app.websocket("/ws")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive_text()
    await websocket.send_text(f"You sent: {data}")
    await websocket.close()


@app.websocket("/ws/{chat_name}")
async def websocket_endpoint(websocket: WebSocket, chat_name: str):
    await websocket.accept()
    if chat_name not in chat_rooms:
        chat_rooms[chat_name] = []
    chat_rooms[chat_name].append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for ws in chat_rooms[chat_name]:
                if ws != websocket:
                    await ws.send_text(data)
    except WebSocketDisconnect:
        chat_rooms[chat_name].remove(websocket)


app.include_router(router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
