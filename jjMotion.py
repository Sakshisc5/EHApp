# pip install opencv-python
# pip install mediapipe

import cv2
import mediapipe as mp
import numpy as np  
import streamlit as st

# MEDIAPIPE INITIALIZATION
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# TEXT DISPLAYED BEFORE OPENING THE CAMERA
st.title("Jumping Jacks Counter")
st.write("Make sure your whole body is in frame for accurate tracking.")
st.write("A window with your camera will open soon, if it doesn't, please refresh the page")

# ANGLE CALCULATOR 
def calculate_angle(a, b, c):
    """Calculates the angle between three points."""
    a = np.array(a)  # FIRST
    b = np.array(b)  # MIDDLE
    c = np.array(c)  # END

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

# VIDEO 
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Camera could not be opened.")
    exit()  

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    count = 0
    stage = "down"

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read from camera.")
            break 

        # COLORS TO RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        results = pose.process(image)

        # RECOLORS TO BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark

            # GET COORDINATES FOR BODY PARTS
            shoulder_left = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y]
            elbow_left = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].y]
            wrist_left = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y]

            shoulder_right = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y]
            elbow_right = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].y]
            wrist_right = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].y]

            # ANGLE CALCULATION
            angle_left = calculate_angle(shoulder_left, elbow_left, wrist_left)
            angle_right = calculate_angle(shoulder_right, elbow_right, wrist_right)

            # WHAT COUNTS AS A JUMPING JACK
            if angle_left < 100 and angle_right < 100 and stage == "down":
                stage = "up"
                count += 1
            if angle_left > 160 and angle_right > 160 and stage == "up":
                stage = "down"

        # KEEPING THIS IN CASE, BUT DOES SEND A LOT OF ERRORS TO THE CMD PROMPT
        # CLOSING THE CMD PROMPT WILL CLOSE THE CAMERA
        except Exception as e:
            print(f"Error extracting landmarks: {e}")  

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))
        
        # TEXT ON THE ACTUAL VIDEO DISPLAY
        count_scale, count_color = 1.5, (255, 0, 0)
        text_scale, text_color = 0.5, (255, 255, 255)
        
        cv2.putText(image, f'Jumping Jacks: {count}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, count_scale, count_color, 2, cv2.LINE_AA)
        cv2.putText(image, "Make sure whole body is in frame", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, text_scale, text_color, 2, cv2.LINE_AA)
        cv2.putText(image, "Open your arms going up",  (10, 100), cv2.FONT_HERSHEY_SIMPLEX, text_scale, text_color, 2, cv2.LINE_AA)
        cv2.putText(image, "Close your arms going down",  (10, 130), cv2.FONT_HERSHEY_SIMPLEX, text_scale, text_color, 2, cv2.LINE_AA)
        cv2.imshow('MediaPipe Pose', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
