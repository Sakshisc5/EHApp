import cv2
import mediapipe as mp
import streamlit as st

# Initialize MediaPipe Pose
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Initialize counter, phase, and previous phase
counter = 0
phase = "closed"  # Track the phase of the movement (open or closed)
previous_phase = "closed"  # Initialize previous_phase to match the starting phase

st.title("Jumping Jack Counter")
st.write("Perform jumping jacks in front of the camera, and the counter will increase.")

# Streamlit video setup
run = st.checkbox('Start Camera')
FRAME_WINDOW = st.image([])

# Method for defining what we count as a jumping jack
def detect_jumping_jack(landmarks):
    global counter, phase, previous_phase

    # Get necessary landmarks
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
    left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
    left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
    right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
    left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
    right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]

    # Calculate distances to determine arm and leg positions
    arms_open = left_wrist.y < left_shoulder.y and right_wrist.y < right_shoulder.y
    legs_open = abs(left_ankle.x - right_ankle.x) > 0.5
    arms_closed = left_wrist.y > left_hip.y and right_wrist.y > right_hip.y
    legs_closed = abs(left_ankle.x - right_ankle.x) < 0.3  # Adjusted threshold for leg closure

    # Check for jumping jack phases
    if arms_open and legs_open:
        phase = "open"  
    elif arms_closed and legs_closed:
        phase = "closed"
    else:
        phase = "in-between"  # New in-between state for transitioning

    # Count jumping jack only if transitioning from "open" to "closed"
    if phase == "closed" and previous_phase == "open":
        counter += 1
        
    # Update the previous phase
    previous_phase = phase

# Video capture and Streamlit loop
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

                # Convert the frame to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(frame)

                # Draw landmarks and detect jumping jacks if landmarks are present
                if results.pose_landmarks:
                    mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                    detect_jumping_jack(results.pose_landmarks.landmark)

                # Show the counter
                cv2.putText(frame, f'Jumping Jacks: {counter}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                
                # Update the Streamlit image with the current frame
                FRAME_WINDOW.image(frame)

        cap.release()
        pose.close()

st.write("Camera Stopped.")


'''
import cv2
import mediapipe as mp
import numpy as np  # Ensure numpy is imported for calculations

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    """Calculates the angle between three points."""
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Camera could not be opened.")
    exit()  # Exit if the camera cannot be accessed

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    count = 0
    stage = "down"

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read from camera.")
            break  # Break the loop if frame reading fails

        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make detection
        results = pose.process(image)

        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark

            # Get coordinates
            shoulder_left = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y]
            elbow_left = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].y]
            wrist_left = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y]

            shoulder_right = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y]
            elbow_right = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].y]
            wrist_right = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].y]

            # Calculate angles
            angle_left = calculate_angle(shoulder_left, elbow_left, wrist_left)
            angle_right = calculate_angle(shoulder_right, elbow_right, wrist_right)

            # Jumping jack logic
            if angle_left < 100 and angle_right < 100 and stage == "down":
                stage = "up"
                count += 1
            if angle_left > 160 and angle_right > 160 and stage == "up":
                stage = "down"

        except Exception as e:
            print(f"Error extracting landmarks: {e}")  # Log any error in landmark extraction

        # Render detections
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

        cv2.putText(image, f'Jumping Jacks: {count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow('MediaPipe Pose', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
'''
''' 
import cv2
import mediapipe as mp
import streamlit as st

# THIS IS THE MEDIAPIPE POSE DETECTOR
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Initialize counter, phase, and previous phase
counter = 0
phase = "closed"  # Track the phase of the movement (open or closed)
previous_phase = "closed"  # Initialize previous_phase to match the starting phase

st.title("Jumping Jack Counter")
st.write("Perform jumping jacks in front of the camera, and the counter will increase.")

# STREAMLIT VIDEO SETUP
run = st.checkbox('Start Camera')
FRAME_WINDOW = st.image([])

# METHOD FOR DEFINING WHAT WE COUNT AS A JUMPING JACK
def detect_jumping_jack(landmarks):
    global counter, phase, previous_phase

    # Get necessary landmarks
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
    left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
    left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
    right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
    left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
    right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]

    # Calculate distances to determine arm and leg positions
    arms_open = left_wrist.y < left_shoulder.y and right_wrist.y < right_shoulder.y
    legs_open = abs(left_ankle.x - right_ankle.x) > 0.5
    arms_closed = left_wrist.y > left_hip.y and right_wrist.y > right_hip.y
    legs_closed = abs(left_ankle.x - right_ankle.x) < 0.3  # Adjusted threshold for leg closure

    # Check for jumping jack phases
    if arms_open and legs_open:
        phase = "open"  
    elif arms_closed and legs_closed:
        phase = "closed"
    else:
        phase = "in-between"  # New in-between state for transitioning

    # Count jumping jack only if transitioning from "open" to "closed"
    if phase == "closed" and previous_phase == "open":
        counter += 1
        
    # Update the previous phase
    previous_phase = phase

# VIDEO CAPTURE AND STREAMLIT LOOP
if run:
    cap = cv2.VideoCapture(0)
    while run and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.write("Unable to access camera.")
            break

        # THIS IS PUTTING THE VIDEO IN COLOR
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame)

        # Draw landmarks and detect jumping jacks if landmarks are present
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            detect_jumping_jack(results.pose_landmarks.landmark)

        # SHOW THE COUNTER
        cv2.putText(frame, f'Jumping Jacks: {counter}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        
        # Update the Streamlit image with the current frame
        FRAME_WINDOW.image(frame)

    cap.release()
    pose.close()

st.write("Camera Stopped.")
'''