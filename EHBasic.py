import streamlit as st
import time

# Load CSS file
with open('C:\\Users\\aasha\\OneDrive\\Hackathon\\hackathon styling.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Check if the welcome page has been shown
if 'welcome_shown' not in st.session_state:
    st.session_state.welcome_shown = False

# Function to update page on submit or Enter
def update_page():
    st.session_state.updated = True

# Welcome Page
if not st.session_state.welcome_shown:
    st.title("Welcome to the Exercise Help App")
    st.markdown("<p style='font-size: 1.5rem; text-align: center;'>Xxxx</p>", unsafe_allow_html=True)  # Placeholder for description

    if st.button("Begin Your Fitness Journey", key="begin"):
        st.session_state.welcome_shown = True
        update_page()
else:
    # Define exercise options for the goal
    exercise_dict = {
        "Weight Loss": ["Running", "Cycling", "HIIT", "Jump Rope", "Swimming"],
        "Muscle Gain": ["Weight Lifting", "Push-ups", "Pull-ups", "Deadlifts", "Squats"],
        "Flexibility": ["Yoga", "Pilates", "Stretching", "Tai Chi", "Dance"],
        "Cardio Fitness": ["Jogging", "Rowing", "Boxing", "Elliptical", "Stair Climber"],
    }

    # Initialize state variables for each question
    if 'name' not in st.session_state:
        st.session_state.name = None
    if 'age' not in st.session_state:
        st.session_state.age = None
    if 'weight' not in st.session_state:
        st.session_state.weight = None
    if 'height' not in st.session_state:
        st.session_state.height = None
    if 'goal' not in st.session_state:
        st.session_state.goal = None

    st.title("Exercise Help App")

    # Step 1: Ask for Name
    def submit_name():
        if st.session_state["name_input"]:
            st.session_state.name = st.session_state["name_input"]
            update_page()

    if st.session_state.name is None:
        st.text_input("What is your name?", key="name_input", on_change=submit_name)
        if st.button("Submit Name"):
            submit_name()
    else:
        st.write(f"**Name:** {st.session_state.name}")

    # Step 2: Ask for Age after Name is entered
    def submit_age():
        if 0 <= st.session_state["age_input"] <= 110:
            st.session_state.age = st.session_state["age_input"]
            update_page()
        else:
            st.warning("Please enter a valid age between 0 and 110.")

    if st.session_state.name and st.session_state.age is None:
        st.number_input("How old are you?", min_value=0, max_value=110, step=1, key="age_input", on_change=submit_age)
        if st.button("Submit Age"):
            submit_age()
    elif st.session_state.age is not None:
        st.write(f"**Age:** {st.session_state.age}")

    # Step 3: Ask for Weight after Age is entered
    def submit_weight():
        if 20 <= st.session_state["weight_input"] <= 1000:
            st.session_state.weight = st.session_state["weight_input"]
            update_page()
        else:
            st.warning("Please enter a valid weight between 20 lbs and 1000 lbs.")

    if st.session_state.age is not None and st.session_state.weight is None:
        st.number_input("What is your weight (in lbs)?", min_value=20, max_value=1000, step=1, key="weight_input", on_change=submit_weight)
        if st.button("Submit Weight"):
            submit_weight()
    elif st.session_state.weight is not None:
        st.write(f"**Weight:** {st.session_state.weight} lbs")

    # Step 4: Ask for Height after Weight is entered
    def submit_height():
        height_value = st.session_state["height_input"]
        try:
            feet, inches = height_value.split("'")
            feet, inches = int(feet), int(inches)
            if 0 <= feet <= 13 and 0 <= inches < 12:
                st.session_state.height = f"{feet}'{inches}"
                update_page()
            else:
                st.warning("Please enter a valid height between 0 and 13 feet, with inches less than 12.")
        except ValueError:
            st.warning("Please enter height in the format: X'Y (e.g., 5'4)")

    if st.session_state.weight and st.session_state.height is None:
        st.text_input("What is your height (in feet and inches)? (Format: 5'4)", key="height_input", on_change=submit_height)
        if st.button("Submit Height"):
            submit_height()
    elif st.session_state.height is not None:
        st.write(f"**Height:** {st.session_state.height}")

    # Step 5: Ask for Exercise Goal after Height is entered
    def submit_goal():
        if st.session_state["goal_input"] != "Select":
            st.session_state.goal = st.session_state["goal_input"]
            update_page()

    if st.session_state.height and st.session_state.goal is None:
        st.selectbox("What is your main exercise goal?", ["Select"] + list(exercise_dict.keys()), key="goal_input", on_change=submit_goal)
        if st.session_state.goal is None and st.button("Submit Goal"):
            submit_goal()
    elif st.session_state.goal is not None:
        st.write(f"**Exercise Goal:** {st.session_state.goal}")

    # Display Recommended Exercises if all inputs are provided
    if st.session_state.goal:
        st.subheader("Recommended Exercises:")
        for exercise in exercise_dict[st.session_state.goal]:
            st.write(f"- {exercise}")