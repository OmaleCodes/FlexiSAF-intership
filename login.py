import streamlit as st
from register import Signup

class User(Signup):

  def get_login():

    self.User_name = st.text_input("Enter your username: ")
    self.__Password = int(st.text_input("Enter your password: "))
    return f"welcome back {self.User_name}"