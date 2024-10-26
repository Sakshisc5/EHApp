# RUN THIS BEFORE RUNNING: pip install opencv-python

import streamlit as st
import cv2
import numpy as np

st.title("Exercise Help App - Pull-Up Form Checker")

# Open video stream
cap = cv2.VideoCapture(0)
FRAME_WINDOW = st.image([])

# Set a reference position for checking "above bar" movement
# For simplicity, we assume the person's head is detected as the highest point
reference_position = None

def process_frame(frame):
    # Convert frame to grayscale and apply Gaussian blur for smoother edges
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
            st.write("Good pull-up! Chin is above the bar.")
        else:
            st.write("Try to pull up higher to get your chin above the bar.")

    return edges  # Display edges for visibility

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Process each frame and get feedback
    edges = process_frame(frame)

    # Display the edges in Streamlit for visibility
    FRAME_WINDOW.image(edges, channels="GRAY")

cap.release()
