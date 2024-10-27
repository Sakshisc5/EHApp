import streamlit as st
from workout import home_page
from sign_in import signin_page
from jjMotion import jjMotion_page
from pMotion import pMotion_page
from bcMotion import bcMotion_page

def main():
    # Initialize the session state if it doesn't exist
    if 'page' not in st.session_state:
        st.session_state.page = "workout"  # Default to home page

    # Render the appropriate page based on session state
    if st.session_state.page == "workout":
        home_page()
    elif st.session_state.page == "sign_in":
        signin_page()
    elif st.session_state.page == "Jumping Jacks Counter":
        jjMotion_page()
    elif st.session_state.page == "Plank Checker":
        pMotion_page()
    elif st.session_state.page == "Bicep Curl Form":
        bcMotion_page()

if __name__ == "__main__":
    main()

