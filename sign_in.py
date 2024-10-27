import pandas as pd
import streamlit as st

file_path = "./workout_users.xlsx"

# Load user data from Excel
def load_user_data(file_path):
    try:
        return pd.read_excel(file_path)
    except Exception as e:
        st.error("Error loading user data: " + str(e))
        return None

# Sign in function
def sign_in(email, password, user_data):
    user = user_data[user_data['Email'] == email]
    if not user.empty:
        if user['Password'].values[0] == password:
            return user.iloc[0]  # Return the first matched user
    return None

# Main app
def signin_page():
    # Set background image
    st.markdown(
        """
        <style>
            .stApp {
                background-image: url("https://img.freepik.com/premium-photo/room-with-bench-bench-with-sun-shining-wall_1086760-231448.jpg");
                background-size: cover; /* Cover the entire viewport */
                background-position: center; /* Center the image */
                background-repeat: no-repeat; /* Prevent tiling */
                height: 100vh; /* Full viewport height */
                color: white; /* Change text color for visibility */
            }

            /* Title color */
            h1 {
                color: #25a6fb !important;  /* Medium Blue title */
                font-size: 41px !important;  /* Larger font size */
                text-align: center;
            }

            /* Logo styling */
            .logo {
                width: 200px; /* Adjust size as needed */
                height: auto;
                position: fixed; /* Fix the logo in the corner */
                top: 50px; /* Adjust as necessary for spacing */
                left: 3px; /* Adjust as necessary for spacing */
                z-index: 10; /* Ensure it stays above other elements */
            }

            /* Button styling */
            .stButton>button {
                background-color: #25a6fb !important; /* Medium Blue */
                color: #ffffff !important;
                border: 1px solid #ffffff;
                border-radius: 8px;
                padding: 10px 20px;
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

    # Container for welcome message
    

    # Sign In Form

    st.title("Sign In")
    
    # Load user data
    user_data = load_user_data(file_path)

    if user_data is not None:
        email = st.text_input("Email", "")
        password = st.text_input("Password", "", type='password')

        if st.button("Sign In"):
            user_info = sign_in(email, password, user_data)
            if user_info is not None:
                st.success("Sign in successful!")
                st.subheader("User Information:")
                st.write(f"**Name:** {user_info['Name']}")
                st.write(f"**Age:** {user_info['Age']}")
                st.write(f"**Height(inches):** {user_info['Height(inches)']} inches")
                st.write(f"**Weight(lbs):** {user_info['Weight(lbs)']} lbs")
                st.write(f"**Goal:** {user_info['Goal']}")
                st.write(f"**Recommended Exercises:** {user_info['Recommended Exercises:']}")
            else:
                st.error("Invalid email or password.")
        if st.button("Back"):
            st.session_state.page = "workout"

    st.markdown("</div>", unsafe_allow_html=True)  # Close the sign-in form container

if __name__ == "__main__":
    signin_page()
