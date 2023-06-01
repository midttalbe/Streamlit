import streamlit as st
from src.router import redirect
from PIL import Image
from  src.controllers import auth as c_auth

import utils as utl

def load_sidebar():

    utl.inject_custom_css()

    mode = "DEMO"

    image = Image.open("src/images/image_booking.jpg")
    
    if mode == "DEMO":
        username = "DEMO MODE"
    else:
        username = c_auth.getUserName().capitalize()

    # st.markdown("""<div align="center" >""",unsafe_allow_html=True)
    st.image(image, channels="RGB", output_format="auto",use_column_width=True)
    utl.navbar_component()
    # st.markdown("""</div>""",unsafe_allow_html=True)
    st.info(f"💻 Vous êtes connecté en tant qu'utilisateur **{username}** ") 


         
 


