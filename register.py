import streamlit as st
class Signup:
    def __init__(self):
        self.User_name = ""
        self.Full_name = ""
        self.__Password = None

    def get_user(self):
        st.write("Fill in the neccessary information to create you account easily")

        self.User_name = st.text_input("Enter your User/Nickname: ")
        self.Full_name = st.text_input("Enter your Full Name: ")

        #exception handlng so int value password is enters and not alphabets  or special numbers
        while True:
            try:
                self.__Password = int(st.text_input("Enter your password(Numbers only): "))
                
                break
            
            except ValueError:
                st.write("Only Numbers are currently accepted")

        return f"Registeration Successful with Username {self.User_name} and Full_name {self.Full_name}"
        exit()
