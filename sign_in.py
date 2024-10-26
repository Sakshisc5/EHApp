import pandas as pd
import streamlit as st

file_path = "/Users/sakshichavan/Desktop/workout_users.xlsx"

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
    st.title("Sign In")

    # Load user data
    user_data = load_user_data('/Users/sakshichavan/Desktop/workout_users.xlsx')

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
                st.write(f"**Height(ft):** {user_info['Height(ft)']} ft")
                st.write(f"**Weight(lbs):** {user_info['Weight(lbs)']} lbs")
                st.write(f"**Goal:** {user_info['Goal']}")
                st.write(f"**Recommended Exercises:** {user_info['Recommended Exercises:']}")
            else:
                st.error("Invalid email or password.")

    if st.button("Back to Sign Up"):
        st.session_state.page = "workout"

if __name__ == "__main__":
    signin_page()