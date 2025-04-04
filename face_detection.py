from fastapi import APIRouter, HTTPException, Query
from starlette.responses import StreamingResponse  
import cv2
import mediapipe as mp
import numpy as np
from typing import List

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

@face_detection_router.get("/video_feed")
async def video_feed(selected_points: List[str] = Query(None)):
    cap = cv2.VideoCapture(0)

    def generate_frames():
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = face_mesh.process(frame_rgb)

            if result.multi_face_landmarks:
                for face_landmarks in result.multi_face_landmarks:
                    mp_drawing.draw_landmarks(
                        image=frame,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
                    )
                    
                    # Draw selected injection points
                    h, w, _ = frame.shape
                    if selected_points:
                        for name in selected_points:
                            if name in INJECTION_POINTS:
                                for idx in INJECTION_POINTS[name]:
                                    if idx < len(face_landmarks.landmark):
                                        landmark = face_landmarks.landmark[idx]
                                        x, y = int(landmark.x * w), int(landmark.y * h)
                                        cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
                                        cv2.putText(frame, name, (x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.25, (0, 255, 0), 1)

            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")
