import streamlit as st
import time

with open('/Users/sakshichavan/Desktop/styles.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

exercise_dict = {
    "Weight Loss": ["Jumping Jacks"],
    "Muscle Gain": ["Bicep Curl"],
    "Abs": ["Plank"],
}

st.title("Exercise Help App")

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
    weight = st.number_input("What is your weight (in lbs)?", min_value=0.1)
if name and age and weight:
    height = st.number_input("What is your height (in ft)?", min_value=0.1)

if name and age and weight and height:
    goal = st.selectbox("What is your main exercise goal?", list(exercise_dict.keys()))

# Submit button
if st.button("Submit"):
    st.write(f"**Name:** {name}")
    st.write(f"**Age:** {age}")
    st.write(f"**Weight:** {weight} kg")
    st.write(f"**Height:** {height} cm")
    st.write(f"**Exercise Goal:** {goal}")
    st.subheader("Recommended Exercises:")
    for exercise in exercise_dict[goal]:
        st.write(f"- {exercise}")
