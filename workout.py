import streamlit as st
import time
import pandas as pd
import os

def home_page():

    user_data_list= []

    with open('/Users/sakshichavan/Desktop/styles.css') as f:
        css = f.read()

    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)


    exercise_dict = {
        "Weight Loss": ["Jumping Jacks"],
        "Muscle Gain": ["Bicep Curl"],
        "Abs": ["Plank"],
    }

    st.title("Exercise Help App")

    if st.button("Sign In"):
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
        height = st.number_input("What is your height (in ft)?", min_value=0.1)
    if name and age and email and password and weight and height:
        goal = st.selectbox("What is your main exercise goal?", list(exercise_dict.keys()))

    # Submit button
    if name and age and email and password and weight and height and goal and st.button("Submit"):
        st.write(f"**Name:** {name}")
        st.write(f"**Age:** {age}")
        st.write(f"**Email:** {email}")
        st.write(f"**Weight:** {weight} lbs")
        st.write(f"**Height:** {height} ft")
        st.write(f"**Exercise Goal:** {goal}")
        st.subheader("Recommended Exercises:")
        for exercise in exercise_dict[goal]:
            st.write(f"- {exercise}")

        user_data_list = {
            "Name": name,
            "Age": age,
            "Email": email,
            "Password": password,
            "Height(ft)": height,
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

