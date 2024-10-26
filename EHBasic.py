import streamlit as st
import time

exercise_dict = {
    "Weight Loss": ["Running", "Cycling", "HIIT", "Jump Rope", "Swimming"],
    "Muscle Gain": ["Weight Lifting", "Push-ups", "Pull-ups", "Deadlifts", "Squats"],
    "Flexibility": ["Yoga", "Pilates", "Stretching", "Tai Chi", "Dance"],
    "Cardio Fitness": ["Jogging", "Rowing", "Boxing", "Elliptical", "Stair Climber"],
}

st.title("Exercise Help App")

placeholder = st.empty()
with placeholder.container():
    st.write("Welcome to our exercise help app!"
    time.sleep(3)
    st.experimental_rerun()

with placeholder.container():
    st.write("Before we help you out, we need a little information :)"
    time.sleep(3)
    st.experimental_rerun()

name = st.text_input("What is your name?")
if name:
    age = st.number_input("How old are you?", min_value=0)
if name and age:
    weight = st.number_input("What is your weight (in lbs)?", min_value=0.0)
if name and age and weight:
    height = st.number_input("What is your height (in cm)?", min_value=0.0)

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
