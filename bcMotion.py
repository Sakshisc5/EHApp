import cv2
import mediapipe as mp
import numpy as np
import streamlit as st

def bcMotion_page():
    st.markdown(
        """
        <style>
            /* Page background color */
            .stApp {
                background-image: url("https://img.freepik.com/premium-photo/blurry-gym-background-with-modern-sports-equipment-fitness-center-concept-gym-photography-blurry-background-fitness-center-modern-equipment_918839-75018.jpg");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                height: 100vh; /* Ensures the background covers the full height */
            }
            /* Title color */
            h1 {
                color: #ffffff !important;  /* White title */
                font-size: 41px !important;  /* Larger font size */
                text-align: center;
            }
            p, label {
                color: #ffffff !important;  /* White text for all paragraphs and labels */
                font-size: 18px !important;  /* Larger font size */
            }
            /* Custom button styles */
            .stButton > button {
                background-color: red; /* Red background */
                color: white; /* White text */
                border: none; /* No border */
                padding: 10px 20px; /* Padding for the button */
                font-size: 18px; /* Font size */
                font-weight: bold; /* Bold text */
                cursor: pointer; /* Pointer cursor on hover */
                border-radius: 5px; /* Rounded corners */
            }
            .stButton > button:hover {
                background-color: darkred; /* Darker red on hover */
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # MEDIAPIPE INITIALIZATION
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    
    # TEXT DISPLAYED BEFORE OPENING THE CAMERA
    st.title("Bicep Curl Checker")
    st.write("Make sure only your arm is visible in the frame for accurate tracking.")
    st.write("A window with your camera will open soon, if it doesn't, please refresh the page.")
    st.write("Press Stop to end the program")
    if st.button("Back"):
            st.session_state.page = "workout"
    
    # ANGLE CALCULATOR (COSINE RULE)
    def calculate_angle(a, b, c):
        a = np.array(a)  
        b = np.array(b)  
        c = np.array(c)  
    
        ab = a - b
        bc = c - b
    
        cos_angle = np.dot(ab, bc) / (np.linalg.norm(ab) * np.linalg.norm(bc))
        cos_angle = np.clip(cos_angle, -1.0, 1.0)
    
        angle = np.arccos(cos_angle) * (180.0 / np.pi)  
        return angle
    
    # VIDEO
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Camera could not be opened.")
        exit()
    
    # INITIAL VARIABLES 
    feedback = "Position Unknown"
    tips = "Position your camera so that only your arm is visible."
    count = 0  
    arm_angle = 0  
    in_curl = False
    
    with mp_pose.Pose(min_detection_confidence=0.3, min_tracking_confidence=0.3) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Error: Unable to read from camera.")
                break
    
            # CHANGE TO RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
    
            # CHANGE BACK TO BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
            try:
                landmarks = results.pose_landmarks.landmark
    
                # ONLY 3 RELEVANT BODY COORDINATES
                shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y]
                elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].y]
                wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].y]
    
                arm_angle = calculate_angle(shoulder, elbow, wrist)
    
                # WHAT COUNTS AS A CURL
                if 160 < arm_angle < 180:  
                    feedback = "Extend your arm completely."
                    in_curl = False  
                    tips = ["Try to fully extend your arm each time. Be slow"]
    
                elif 30 < arm_angle < 60:  
                    if not in_curl:  
                        count += 1  
                        in_curl = True  # THIS IS BASICALLY BEGINNING OF THE CURL
                    feedback = "Great contraction!"
                    tips = ["Control your movement for the best results."]
    
                else:
                    feedback = "Maintain controlled motion."
                    tips = ["Keep the movement steady and avoid swinging."]
    
            except Exception as e:
                print(f"Error extracting landmarks: {e}")
    
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))
    
            # EVERYTHING DISPLAYED ON THE ACTUAL VIDEO
            text_scale, text_color = 0.5, (0, 0, 255)
            cv2.putText(image, feedback, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, text_scale, (0, 255, 0) if in_curl else (0, 0, 255), 1, cv2.LINE_AA)
            cv2.putText(image, f'Curls Count: {count}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, text_scale, text_color, 1, cv2.LINE_AA)
            cv2.putText(image, f'Arm Angle: {int(arm_angle)} degrees', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, text_scale, text_color, 1, cv2.LINE_AA)
    
            # TIPS
            y_offset = 130
            for tip in tips:
                cv2.putText(image, tip, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, text_scale, text_color, 1, cv2.LINE_AA)
                y_offset += 30
    
            cv2.imshow('Bicep Curl Checker', image)
    
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
    
        cap.release()
        cv2.destroyAllWindows()
if __name__ == "__main__":
    bcMotion_page()
