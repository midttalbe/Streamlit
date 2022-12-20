import streamlit as st
from src.views import a_login as login, b_home as home, c_objectif as objectif, d_presentation as presentation, e_analyse as analyse, f_conclusions as conclusions
from src.router import redirect, get_route
from src.controllers import auth as c_auth
from src.controllers.analyse import Analyse
# import utils as utl

st.set_page_config(layout="wide", page_title='Projet d\'analyse de données',menu_items={
'Get Help': 'https://www.extremelycoolapp.com/help',
'Report a bug': "https://www.extremelycoolapp.com/bug",
'About': "# This is a header. This is an *extremely* cool app!"
})
st.set_option('deprecation.showPyplotGlobalUse', False)
# utl.inject_custom_css()
# utl.navbar_component()

init = False
if not init:
    # charge données
    Analyse().load()
    init = True

def _max_width_():
    max_width_str = f'max-width: 1000px';

    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>
    """,
        unsafe_allow_html=True,
    ) 


def navigation():

    if c_auth.isAuthenticated():
        # redirect("/b_home", reload=True)
        route = get_route()

        if route == '/b_home':
            username = c_auth.getUserName()
            home.load_view(username)

        elif route == '/c_objectif':
            objectif.load_view()

        elif route == '/d_presentation':
            presentation.load_view()

        elif route == '/e_analyse':
            analyse.load_view()

        elif route == '/f_conclusions':
            conclusions.load_view()

        elif route == '/logout':
            c_auth.deconnexion()
            redirect("/a_login",reload=True)
        else:
            home.load_view()

    else:
        redirect("/a_login")
        login.load_view()

_max_width_()
navigation()
