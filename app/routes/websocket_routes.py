from fastapi import APIRouter, HTTPException, Depends
from fastapi import WebSocket, WebSocketDisconnect
import cv2
import numpy as np
import base64
import mediapipe as mp
import json

router = APIRouter(tags=["Web sockets"])

active_connections=[]
INJECTION_POINTS = {
    "forehead_lines_botox": [10, 151, 338, 67, 107, 336],
    "frown_lines_glabella_botox": [9, 8, 168, 6, 197, 195, 5],
    "crows_feet_botox": [263, 362, 386, 133, 173, 156],
    "nasalis_lines_botox": [98, 327],   # Added approximate bunny line points
    "vertical_lip_lines_botox": [61, 0, 267, 17, 84, 37],  
    "lip_flip_botox": [0, 267, 37, 17, 287, 84],  
    "smile_lift_botox": [61, 76, 91, 305, 290, 409],
    "masseter_reduction_botox": [172, 58],  # Jawline points
    "dimpled_chin_botox": [18, 83, 14],
    "platysmal_bands_botox": [131, 50, 205, 280, 425], # Neck lower landmarks
    "cheek_filler": [
        50, 205, 429,   # Left cheek
        280, 425, 449   # Right cheek
    ],
    "smile_line_filler": [61, 91, 76, 290, 305, 409],
    "lip_filler": [
        0, 267, 37, 17, 287, 84
    ],
    "temple_filler": [26, 54, 226, 247, 110],
    "nose_filler": [4,5,6,248]
}
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

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils


@router.websocket("/cursor")
async def websocket_cursor(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            websocket.cursor_position = (data['x'], data['y'])
    except WebSocketDisconnect:
        active_connections.remove(websocket)




# Cache for smoothing landmark positions
landmark_cache = {}

@router.websocket("/stream")
async def video_ws(websocket: WebSocket):
    await websocket.accept()
    hovered_point = None

    while True:
        data = await websocket.receive_text()
        message = json.loads(data)

        if message["type"] == "frame":
            # print(message.get("points"))
            points_data=json.loads(message.get("points"))
            selected_points=[]
            # print("points_data",points_data)
            for point in points_data:
                # print(point)
                selected_points.append(point["name"])
            # print(selected_points)
            img_data = base64.b64decode(message["frame"])
            nparr = np.frombuffer(img_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = face_mesh.process(frame_rgb)

            landmark_pixel_list = []

            if result.multi_face_landmarks:
                for face_landmarks in result.multi_face_landmarks:
                    h, w, _ = frame.shape
                    for name, indices in INJECTION_POINTS.items():
                        if name not in selected_points:
                            continue  # Skip if not selected

                        for idx in indices:
                            if idx < len(face_landmarks.landmark):
                                lm = face_landmarks.landmark[idx]
                                x, y = int(lm.x * w), int(lm.y * h)

                                # Smooth using cache
                                prev = landmark_cache.get(f"{name}_{idx}")
                                if prev:
                                    x = int(prev[0] * 0.7 + x * 0.3)
                                    y = int(prev[1] * 0.7 + y * 0.3)

                                landmark_cache[f"{name}_{idx}"] = (x, y)
                                landmark_pixel_list.append({
                                    "name": name, 
                                    "index": idx, 
                                    "x": x, 
                                    "y": y
                                })
                                # print(landmark_pixel_list)
                                # Draw point with color based on hover
                                if name == message.get("hovered"):
                                    # print(message.get("hovered"))
                                    color = (0, 0, 255)  # red when hovered
                                    radius = 4
                                else:
                                    color = (0, 255, 0)  # green otherwise
                                    radius = 3

                                cv2.circle(frame, (x, y), radius, color, -1)


            _, buffer = cv2.imencode('.jpg', frame)
            frame_b64 = base64.b64encode(buffer).decode('utf-8')
            await websocket.send_text(json.dumps({
                "frame": frame_b64,
                "landmarks": landmark_pixel_list
            }))

        elif message["type"] == "hover":
            hovered_point = message.get("hovered")
