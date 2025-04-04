from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
import cv2
import mediapipe as mp
import numpy as np
import base64
import asyncio
import json

face_detection_router = APIRouter()

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

INJECTION_POINTS = {
    "forehead_botox": [10, 151, 338, 67, 107, 336],
    "glabella_botox": [9, 8, 168, 6, 197, 195, 5],
    "crows_feet_botox": [263, 362, 386, 133, 173, 156],
    "cheek_filler": [50, 205, 425, 429],
    "smile_line_filler": [61, 91, 76, 290, 305, 409],
    "lip_filler": [61, 146, 91, 181, 78, 95],
    "temple_filler": [26, 54, 226, 247, 110, 338],
    "nose_filler": [4, 5, 6, 248]
}

@face_detection_router.get("/", response_class=HTMLResponse)
async def serve_home(request: Request):
    checkboxes = "".join([
        f'<input type="checkbox" name="selected_points" value="{key}"> {key}<br>'
        for key in INJECTION_POINTS.keys()
    ])
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Face Mesh Detection</title>
    </head>
    <body>
        <h1>Face Mesh Detection</h1>
        <button onclick="requestCameraAccess()">Enable Camera</button>
        <video id="videoElement" autoplay playsinline></video>
        <canvas id="canvasElement" style="display:none;"></canvas>
        <img id="processedStream" width="640" height="480" />
        <br>
        <label>Select Injection Points:</label><br>
        {checkboxes}
        <button onclick="updateStream()">Update Stream</button>
        <script>
            const video = document.getElementById("videoElement");
            const canvas = document.getElementById("canvasElement");
            const ctx = canvas.getContext("2d");
            const img = document.getElementById("processedStream");
            const ws = new WebSocket("ws://" + window.location.host + "/ws");
            
            function requestCameraAccess() {{
                navigator.mediaDevices.getUserMedia({{ video: true }})
                    .then(stream => {{
                        video.srcObject = stream;
                    }})
                    .catch(error => {{
                        console.error("Camera access denied:", error);
                    }});
            }}
            
            function getSelectedPoints() {{
                let selected = [];
                document.querySelectorAll('input[name="selected_points"]:checked').forEach(checkbox => {{
                    selected.push(checkbox.value);
                }});
                return selected;
            }}
            
            function sendFrame() {{
                if (video.videoWidth === 0 || video.videoHeight === 0) return;
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                const frameData = canvas.toDataURL("image/jpeg");
                const selectedPoints = getSelectedPoints();
                ws.send(JSON.stringify({{ frame: frameData, points: selectedPoints }}));
            }}
            
            ws.onmessage = function(event) {{
                img.src = event.data;
            }};
            
            function updateStream() {{
                sendFrame();
            }}
            
            setInterval(sendFrame, 100);
        </script>
    </body>
    </html>
    """

@face_detection_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            data_json = json.loads(data)
            frame_data = data_json.get("frame")
            selected_points = data_json.get("points", [])
            
            if not frame_data.startswith("data:image/jpeg;base64,"):
                continue
            frame_bytes = base64.b64decode(frame_data.split(",")[1])
            frame_np = np.frombuffer(frame_bytes, dtype=np.uint8)
            if frame_np.size == 0:
                continue
            frame = cv2.imdecode(frame_np, cv2.IMREAD_COLOR)
            if frame is None:
                continue
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = face_mesh.process(frame_rgb)
            
            if result.multi_face_landmarks:
                h, w, _ = frame.shape
                for face_landmarks in result.multi_face_landmarks:
                    mp_drawing.draw_landmarks(
                        image=frame,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
                    )
                    for key in selected_points:
                        if key in INJECTION_POINTS:
                            for idx in INJECTION_POINTS[key]:
                                x, y = int(face_landmarks.landmark[idx].x * w), int(face_landmarks.landmark[idx].y * h)
                                cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
            
            _, buffer = cv2.imencode('.jpg', frame)
            processed_frame = base64.b64encode(buffer).decode('utf-8')
            await websocket.send_text(f'data:image/jpeg;base64,{processed_frame}')
    except WebSocketDisconnect:
        pass