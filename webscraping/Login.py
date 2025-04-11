import streamlit as st
import time
import re

regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

if "pages" not in st.session_state:
    st.session_state.pages = "login"

if "modals" not in st.session_state:
    st.session_state.modals = "signup"

def email_verification(email):
    return re.fullmatch(regex, email)

@st.dialog("Sign Up")
def signup():
    new_username = st.text_input("Username", placeholder="Enter your username")
    new_email = st.text_input("Email", placeholder="Enter your email id")

    if not (valid_email := email_verification(new_email)) and new_email:
        st.error("Invalid email")

    new_password = st.text_input("Password", placeholder="Enter your password", type="password")
    if(st.button("Create your account")):
        if new_username and new_password and valid_email:
            st.empty()  
            st.write("Check your mail for the verification of your account.")
            time.sleep(2.2)
            st.rerun()
        else:
            st.error("Please enter all the fields")



def login_form():
    st.title("Login")
    with st.form(key = "loginform"):

        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", placeholder="Enter your password", type="password")

        col1, col2 = st.columns(2)

        with col1:
            login_button = st.form_submit_button("Login", use_container_width=True)

        with col2:
            signup_button = st.form_submit_button("Sign Up", use_container_width=True)

        if(login_button or (username and password)):
            if(username == "admin" and password == "1234"):
                st.success("Login successful.")
                st.session_state.username = username
                st.session_state.pages = "home"
                st.rerun()
            else:
                st.error("Invalid login.")

        if(signup_button):
            st.session_state.modals = "signup"
            signup()

def home_page():
    st.title(f"Welcome {st.session_state.username}")
    st.write("Nice to have you!")
    if st.button("Logout"):
        st.error("Logging out.")
        st.session_state.pages = "login"
        time.sleep(0.3)
        st.rerun()

if st.session_state.pages == "login":
    login_form()
else:
    home_page()