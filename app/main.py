from fastapi import FastAPI, HTTPException
from app.utils.functions import handle_exception, create_response
from app.routes.auth_routes import router as auth_router
from fastapi.responses import JSONResponse
from app.routes.procedure_routes import router as procedure_router
from app.routes.image_data_routes import router as image_router
from app.routes.plan_routes import router as plan_router
from app.routes.stripe_routes import router as stripe_routes
from app.routes.admin_user_routes import router as admin_user_router
from fastapi.middleware.cors import CORSMiddleware
from app.routes.websocket_routes import router as websocket_router

app = FastAPI(title="Botox-Injection-Predictor")

origins = [
    "http://localhost:5173"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],             # Allow any origin
    allow_credentials=True,          # Keep this if you use cookies/auth headers
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Botox Injection Predictor"}

app.include_router(auth_router, prefix="/auth")
app.include_router(procedure_router, prefix="/procedures")
app.include_router(admin_user_router, prefix="/admin/users")
app.include_router(image_router, prefix="/image")
app.include_router(stripe_routes, prefix="/stripe")
app.include_router(plan_router, prefix="/api/plans")
app.include_router(websocket_router, prefix="/ws")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return create_response(500,False,"Internal Server Error")


# #websocket
# from fastapi import WebSocket, WebSocketDisconnect
# import cv2
# import numpy as np
# import base64
# import mediapipe as mp
# import json

# active_connections = []

# @app.websocket("/ws/cursor")
# async def websocket_cursor(websocket: WebSocket):
#     await websocket.accept()
#     active_connections.append(websocket)
#     try:
#         while True:
#             data = await websocket.receive_json()
#             websocket.cursor_position = (data['x'], data['y'])
#     except WebSocketDisconnect:
#         active_connections.remove(websocket)

# mp_face_mesh = mp.solutions.face_mesh
# face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
# mp_drawing = mp.solutions.drawing_utils

# INJECTION_POINTS = {
#     "forehead_botox": [10, 151, 338, 67, 107, 336],
#     "glabella_botox": [9, 8, 168, 6, 197, 195, 5],
#     "crows_feet_botox": [263, 362, 386, 133, 173, 156],
#     "cheek_filler": [50, 205, 425, 429],
#     "smile_line_filler": [61, 91, 76, 290, 305, 409],
#     "lip_filler": [61, 146, 91, 181, 78, 95],
#     "temple_filler": [26, 54, 226, 247, 110, 338],
#     "nose_filler": [4, 5, 6, 248]
# }

# # Cache for smoothing landmark positions
# landmark_cache = {}

# @app.websocket("/ws/stream")
# async def video_ws(websocket: WebSocket):
#     await websocket.accept()
#     hovered_point = None

#     while True:
#         data = await websocket.receive_text()
#         message = json.loads(data)

#         if message["type"] == "frame":
#             img_data = base64.b64decode(message["frame"])
#             nparr = np.frombuffer(img_data, np.uint8)
#             frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

#             frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             result = face_mesh.process(frame_rgb)

#             landmark_pixel_list = []

#             if result.multi_face_landmarks:
#                 for face_landmarks in result.multi_face_landmarks:
#                     h, w, _ = frame.shape
#                     for name, indices in INJECTION_POINTS.items():
#                         idx = indices[0]  # only take the first point
#                         if idx < len(face_landmarks.landmark):
#                             lm = face_landmarks.landmark[idx]
#                             x, y = int(lm.x * w), int(lm.y * h)

#                             # Smooth using cache
#                             prev = landmark_cache.get(name)
#                             if prev:
#                                 x = int(prev[0] * 0.7 + x * 0.3)
#                                 y = int(prev[1] * 0.7 + y * 0.3)

#                             landmark_cache[name] = (x, y)
#                             landmark_pixel_list.append({"name": name, "x": x, "y": y})

#                             # Draw the circle with bigger radius
#                             if name == message.get("hovered"):
#                                 color = (0, 0, 255)
#                                 radius = 8
#                             elif hovered_point == name:
#                                 color = (0, 255, 0)
#                                 radius = 8
#                             else:
#                                 color = (0, 255, 0)
#                                 radius = 6
                            
#                             cv2.circle(frame, (x, y), radius, color, -1)

#             _, buffer = cv2.imencode('.jpg', frame)
#             frame_b64 = base64.b64encode(buffer).decode('utf-8')
#             await websocket.send_text(json.dumps({
#                 "frame": frame_b64,
#                 "landmarks": landmark_pixel_list
#             }))

#         elif message["type"] == "hover":
#             hovered_point = message.get("hovered")
