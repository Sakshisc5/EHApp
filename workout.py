import streamlit as st
import time
import pandas as pd
import os

def home_page():
    # Inline CSS for styling
    st.markdown(
        """
        <style>
            /* Page background color */
            .stApp {
        background-image: url("https://webuygymequipment.com/assets/img/gym-equipment-2.webp");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }

            /* Title color */
            h1 {
                color: #25a6fb !important;  /* Medium Blue title */
                font-size: 36px !important;  /* Larger font size */
                text-align: center;
            }

            /* Welcome message styling */
            .welcome-message {
                color: #000000 !important;  /* Medium Blue */
                text-align: center;
                font-size: 18px !important;
            }

            p, label {
                color: #ffffff !important;  /* White text for all paragraphs and labels */
                font-size: 18px !important;  /* Larger font size */
            }

            /* Button styling */
            .stButton>button {
                background-color: #25a6fb !important; /* Medium Blue */
                color: #ffffff !important;
                border: 1px solid #ffffff;
                border-radius: 8px;
                padding: 10px 20px;
                width: 100%;
            }
            .stButton>button:hover {
                background-color: #165cbb !important; /* Darker Blue on hover */
            }

            /* Input fields */
            .stTextInput input, .stNumberInput input {
                background-color: #ffffff !important;
                color: #1059b8 !important; /* Medium Blue */
                border: 2px solid #1059b8;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <div style='background-color: rgba(255, 255, 255, 0.8); padding: 20px; border-radius: 10px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);'>
            <h1>Exercise Help App</h1>
            <p class='welcome-message'>Welcome to the Exercise Help App! Please provide your information below:</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # User data collection code
    user_data_list = []

    exercise_dict = {
        "Weight Loss": ["Jumping Jacks"],
        "Muscle Gain": ["Bicep Curl"],
        "Abs": ["Plank"],
    }
    # Top navigation bar with buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Jumping Jacks Counter", key="jumpingjack"):
            st.session_state.page = "Jumping Jacks Counter"

    
    with col2:
        if st.button("Plank Checker", key="plank"):
            st.session_state.page = "Plank Checker"


    with col3:
        if st.button("Bicep Curl Form", key="bicep"):
            st.session_state.page = "Bicep Curl Form"

    if st.button("Log In"):
        st.session_state.page = "sign_in"

    st.write("Or Sign Up Below")

    if 'show_welcome' not in st.session_state:
        st.session_state.show_welcome = True

    if 'show_info_message' not in st.session_state:
        st.session_state.show_info_message = False

    # Show welcome message
    if st.session_state.show_welcome:
        st.write("Welcome to our exercise help app!")
        time.sleep(2)  # Pause for 2 seconds
        st.session_state.show_welcome = False
        st.session_state.show_info_message = True

    # Show information message
    elif st.session_state.show_info_message:
        st.write("Before we help you out, we need some information.")
        time.sleep(2)  # Pause for another 2 seconds
        st.session_state.show_info_message = False

    # Collect user information
    name = st.text_input("What is your name?")
    if name:
        age = st.number_input("How old are you?", min_value=0)
    if name and age:
        email = st.text_input("Enter your email address:")
    if name and age and email:
        password = st.text_input("Enter a password:", type="password")
    if name and age and email and password:
        weight = st.number_input("What is your weight (in lbs)?", min_value=0.1)
    if name and age and email and password and weight:
        height = st.number_input("What is your height (in inches)?", min_value=0.1)
    if name and age and email and password and weight and height:
        goal = st.selectbox("What is your main exercise goal?", list(exercise_dict.keys()))

    # Submit button
    if name and age and email and password and weight and height and goal and st.button("Submit"):
        st.write(f"**Name:** {name}")
        st.write(f"**Age:** {age}")
        st.write(f"**Email:** {email}")
        st.write(f"**Weight:** {weight} lbs")
        st.write(f"**Height:** {height} inches")
        st.write(f"**Exercise Goal:** {goal}")
        st.subheader("Recommended Exercises:")
        for exercise in exercise_dict[goal]:
            st.write(f"- {exercise}")
        st.button("Scroll up for the needed form checker")

        user_data_list = {
            "Name": name,
            "Age": age,
            "Email": email,
            "Password": password,
            "Height(inches)": height,
            "Weight(lbs)": weight,
            "Goal": goal,
            "Recommended Exercises:": exercise_dict[goal],
        }

        file_path = "./workout_users.xlsx"

        if os.path.exists(file_path):
            # Read existing data
            existing_data = pd.read_excel(file_path)
            # Append the new entry
            updated_data = pd.concat([existing_data, pd.DataFrame([user_data_list])], ignore_index=True)
        else:
            # If the file doesn't exist, create a new DataFrame
            updated_data = pd.DataFrame([user_data_list])

        # Save the updated DataFrame to the Excel file
        updated_data.to_excel(file_path, index=False, engine='openpyxl')

        st.success("Your data has been saved.")

    # Close the main content div
    st.markdown("</div>", unsafe_allow_html=True)
