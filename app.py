import streamlit as st
from register import Signup
from login import User



st.sidebar.header("Welcome to DANGOTE IPO, what would you like to do? ")
st.write("1. Create an Account")
st.write("2. Log into current Account")
st.write("3. Contact support")
st.write("4. Faq & Help")
st.write("5. Exit")

try:
    option = int(st.text_input("Enter your selected option: "))
except:
    e = "Enter a number selection! "
    st.write(e)

#initialization of the registration for users
reg = Signup()

#initialization of the user login
join = User()



if option == 1:
    st.write(reg.get_user())
elif option == 2:
    st.write(join.get_login())
elif option == 3:
    st.write("contact support")
elif option == 4:
    st.write("Faq & Help")
elif option == 5:
    st.write("Exit")
else:
    st.write(option)