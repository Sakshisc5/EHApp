import streamlit as st
import cv2
import numpy as np

st.title("Exercise Help App - Pull-Up Form Checker")

# Initialize video capture
cap = cv2.VideoCapture(0)
FRAME_WINDOW = st.image([])

# Set a reference position for checking "above bar" movement
reference_position = None

def process_frame(frame):
    # Convert frame to grayscale for contour detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (15, 15), 0)

    # Use edge detection
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours in the edge map
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the highest point, assuming it's the head
    max_y = frame.shape[0]
    head_position = None

    for contour in contours:
        # Get bounding box for each contour
        x, y, w, h = cv2.boundingRect(contour)
        
        # If the contour is at a higher position (smaller y), assume it's the head
        if y < max_y and w > 30:  # Filter out noise based on width threshold
            max_y = y
            head_position = y

    # Set a reference position if none exists
    global reference_position
    if reference_position is None and head_position is not None:
        reference_position = head_position + 50  # Approximate starting chin level

    # Display feedback based on position
    if head_position is not None:
        if head_position < reference_position:
            cv2.putText(frame, "Good pull-up! Chin is above the bar.", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Try to pull up higher to get your chin above the bar.", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    return frame  # Return the original frame with annotations

# Button to start/stop video feed
if st.button("Start Video"):
    st.session_state.running = True  # Track if the video is running

# Stop the video stream if button is pressed
if st.button("Stop Video"):
    st.session_state.running = False  # Stop the video loop
    cap.release()

# Continuous video feed display
if st.session_state.get("running", False):
    while True:
        ret, frame = cap.read()
        if not ret:
            st.write("Failed to grab frame.")
            break
        processed_frame = process_frame(frame)
        # Display the original frame in Streamlit
        FRAME_WINDOW.image(processed_frame, channels="BGR")
        
        # Break out of the loop when the video is stopped
        if not st.session_state.get("running", False):
            break

# Release the video capture when the app is stopped
if cap is not None:
    cap.release()
