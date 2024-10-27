import cv2
import mediapipe as mp
import numpy as np
import streamlit as st
import time

# MEDIAPIPE INITIALIZATION
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
color = (0, 0, 0)

# TEXT DISPLAYED BEFORE OPENING THE CAMERA
st.title("Plank Checker")
st.write("Make sure your whole side is in frame for accurate tracking.")
st.write("A window with your camera will open soon; if it doesn't, please refresh the page.")

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

# INITIALIZE THESE VARIABLES SO THEY DON'T CAUSE AN ERROR WHEN THE PAGE IS LOADED 
feedback = "Position Unknown"
tips = "Place your camera in a good position."
count = 0  
shoulder_angle = 0
hip_angle = 0 

with mp_pose.Pose(min_detection_confidence=0.3, min_tracking_confidence=0.3) as pose:
    start_time = None  
    duration = 0  # HOW LONG THE USER IS IN PROPER POSITION 
    in_plank = False  # BOOLEAN FOR CHECKING IF THE USER IS IN THE RIGHT POSITION 

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

            hip_left = [landmarks[mp_pose.PoseLandmark.LEFT_HIP].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP].y]
            hip_right = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP].y]
        

            #HIP ANGLE IS NOT CALCULATED USING THE KNEE BECAUSE BEGINNER PLANKS HAVE THE KNEE ON THE FLOOR
            shoulder_angle = calculate_angle(shoulder_left, elbow_left, wrist_left)
            hip_angle = calculate_angle(hip_left, shoulder_left, hip_right)


            # DRAW VISUAL LINES (FOR DEBUGGING)
            cv2.line(image, tuple(np.multiply(shoulder_left, [image.shape[1], image.shape[0]]).astype(int)),
                     tuple(np.multiply(elbow_left, [image.shape[1], image.shape[0]]).astype(int)), (255, 255, 255), 2)
            cv2.line(image, tuple(np.multiply(elbow_left, [image.shape[1], image.shape[0]]).astype(int)),
                     tuple(np.multiply(wrist_left, [image.shape[1], image.shape[0]]).astype(int)), (255, 255, 255), 2)

            cv2.line(image, tuple(np.multiply(hip_left, [image.shape[1], image.shape[0]]).astype(int)),
                     tuple(np.multiply(shoulder_left, [image.shape[1], image.shape[0]]).astype(int)), (255, 255, 255), 2)
            cv2.line(image, tuple(np.multiply(shoulder_left, [image.shape[1], image.shape[0]]).astype(int)),
                     tuple(np.multiply(hip_right, [image.shape[1], image.shape[0]]).astype(int)), (255, 255, 255), 2)

            # CHECK IF THE USER IS IN A PROPER PLANK POSITION
            #OPTIMIZED FOR BOTH BEGINNER AND PROFESSIONAL PLANKS
            if 90 < shoulder_angle < 115 and 0 < hip_angle < 5:  # THRESHOLDS ARE LENIENT BECAUSE THE LANDMARKS ARE CURRENTLY INCONSISTENT
                if not in_plank:  
                    start_time = time.time()  
                in_plank = True  

                duration = time.time() - start_time

                # THE PLANK IS COUNTED AS A PLANK IF IT LASTS 15 SECONDS OR LONGER
                if duration >= 15 and in_plank:
                    count += 1  
                    start_time = time.time()
                    in_plank = False
                # TIPS FOR GOOD POSITION
                tips = [
                    "Keep your head aligned with your spine.",
                    "Engage your core and keep your back straight."
                ]
                feedback = "Good Plank Position!"
                color = (0, 255, 0)  
            else:
                feedback = "Adjust Your Position!"
                color = (0, 0, 255)  
                in_plank = False

                # RESETS DURATION IF USER IS NOT IN PLANK 
                start_time = None  
                duration = 0  

                # TIPS FOR WRONG POSITION 
                tips = ["Focus on maintaining a straight line from head to heels."]

        except Exception as e:
            print(f"Error extracting landmarks: {e}")

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

        # TEXT ON THE ACTUAL VIDEO DISPLAY
        text_scale, text_color = 0.5, (0, 0, 0)

        cv2.putText(image, feedback, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, text_scale, color, 1, cv2.LINE_AA)
        cv2.putText(image, f'Duration: {int(duration)} seconds', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, text_scale, text_color, 1, cv2.LINE_AA)
        cv2.putText(image, f'Planks Held (15 Seconds): {count}', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, text_scale, text_color, 1, cv2.LINE_AA)

        # DEBUGGING CODE (CHECK SHOULDER ANGLE TO SEE IF PLANK IS CALCULATED RIGHT)
        cv2.putText(image, f'Shoulder Angle: {shoulder_angle}, Hip Angle: {hip_angle}', (10, 450), cv2.FONT_HERSHEY_SIMPLEX, text_scale, (255, 0, 0), 1, cv2.LINE_AA)


        # CODE THAT DISPLAYS TIPS
        y_offset = 130
        for tip in tips:
            cv2.putText(image, tip, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, text_scale, text_color, 1, cv2.LINE_AA)
            y_offset += 30

        cv2.imshow('MediaPipe Pose', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
