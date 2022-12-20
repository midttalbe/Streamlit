import streamlit as st
from  src.controllers import auth as c_auth
from src.views.components import side_bar

def load_view():
    
    side_bar.load_sidebar()
    
    st.title("Conclusions")
    st.subheader("1) ...")
    st.subheader("2) ...")