import streamlit as st
from workout import home_page
from sign_in import signin_page

def main():
    st.markdown('<link rel="stylesheet" href="stylesheet.css">', unsafe_allow_html=True)

    # Initialize the session state if it doesn't exist
    if 'page' not in st.session_state:
        st.session_state.page = "workout"  # Default to home page

    # Render the appropriate page based on session state
    if st.session_state.page == "workout":
        home_page()
    elif st.session_state.page == "sign_in":
        signin_page()

if __name__ == "__main__":
    main()
