import cv2
import mediapipe as mp
import streamlit as st

# MEDIAPIPE INITIALIZATION
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


counter = 0
phase = "closed"  
previous_phase = "closed"  

st.title("Jumping Jack Counter")
st.write("Perform jumping jacks in front of the camera, and the counter will increase.")

# VIDEO 
run = st.checkbox('Start Camera')
FRAME_WINDOW = st.image([])

# WHAT WE COUNT AS A JUMPING JACK
def jumping_jack(landmarks):
    global counter, phase, previous_phase

    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
    left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
    left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
    right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
    left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
    right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]

    # ARM AND LEG POSITION CODE
    arms_open = left_wrist.y < left_shoulder.y and right_wrist.y < right_shoulder.y
    legs_open = abs(left_ankle.x - right_ankle.x) > 0.5
    arms_closed = left_wrist.y > left_hip.y and right_wrist.y > right_hip.y
    legs_closed = abs(left_ankle.x - right_ankle.x) < 0.3  # Adjusted threshold for leg closure

    # JUMPING JACK PHASES 
    if arms_open and legs_open:
        phase = "open"  
    elif arms_closed and legs_closed:
        phase = "closed"
    else:
        phase = "in-between"  

    # A JUMPING JACK IS WHEN WE GO FROM CLOSED TO OPEN 
    if phase == "closed" and previous_phase == "open":
        counter += 1
        

    previous_phase = phase

# HOW WE RUN THE VIDEO ON STREAMLIT USING OPENCV
if run:
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        st.write("Error: Camera could not be opened.")
    else:
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while run and cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    st.write("Unable to access camera.")
                    break

                # MAKE THE VIDEO HAVE COLOR 
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(frame)

                if results.pose_landmarks:
                    mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                    jumping_jack(results.pose_landmarks.landmark)

     
                cv2.putText(frame, f'Jumping Jacks: {counter}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                
                FRAME_WINDOW.image(frame)

        cap.release()
        pose.close()

st.write("Camera Stopped.")


