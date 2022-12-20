import streamlit as st
from src.views.components import side_bar
from PIL import Image

def load_bienvenue():
    st.title("Bienvenue sur mon site") 

    st.subheader("Qui suis-je ?")
    st.markdown("""
    <p>
    Je m'appelle <b>Mohamed IDTTALBE</b>, 42 ans et j'ai plus de 15 d'expériences dans le domaine informatique.

    Je suis spécialisé dans les systèmes de bases de données et dans le language SQL.

    Dans le cadre d'une mise à jour de mes compétences, j'ai effectué une <b>formation BOOTCAMP de Data Analyste</b> au sein de l'organisme de formation <b>DATAROCKSTARS</b>.

    La création de ce site vient clôturer ma formation et permet de voir toutes les compétences acquises au sein de ce bootcamp.
    </p>
    <div align="center">
    <img class="logo logo-dark ls-is-cached lazyloaded" alt="logo" src="https://www.datarockstars.ai/wp-content/uploads/2022/07/logo-datarockstars.png" data-src="https://www.datarockstars.ai/wp-content/uploads/2022/07/logo-datarockstars.png" decoding="async" width="285" height="50">
    </div>
    <div align="center">
    <b><a href=https://www.datarockstars.ai/data-analyst/ >Lien vers la formation</a></b>
    </div><br>
    <p>
    Si vous avez des remarques ou autres suggestions concernant ce site ou bien pour me proposer des offres de missions, je suis joignable : 

    <ul>
        <li>via email : <a href= "mailto:mohamed.idttalbe@outlook.fr" >mohamed.idttalbe@outlook.fr</a></li>
        <li>via ma page LinkedIn : ?</li>
    </ul>

    Je vous souhaite bonne lecture 🙂.
    </p>
    """,unsafe_allow_html=True)

def load_que_peut_on_voir():
    st.subheader("Que peut-on voir sur ce site ?")
    st.markdown("""
    Ce site permet de visualiser une analyse concernant des réservations d'hotel.

    Cette analyse a été réalisé à l'aide des outils suivants :\n
        - langage Python pour la conception du programme
        - librairie Pandas pour la transformation de données
        - librairie Matplotlib et Seaborn pour les graphiques
        - modèle MVC pour le site internet
    """)


def load_pourquoi_python():
    st.subheader("Pourquoi Python ?")

    image = Image.open("src/images/logo_python.png")
    st.image(image, width=100)

    st.markdown("""
    Le langage Python est devenue depuis ces dernières années le langage préférentiel en ce qui concerne les analyses de données.
    En effet, il est facile d'apprentissage et inclus plusieurs librairies adaptées à l'analyse de données.
    """
    )

def load_view(username = ""):
    col_a,col_b,col_c = st.columns([1,4,1])
    with col_b:
        side_bar.load_sidebar()
        
        load_bienvenue()
        load_que_peut_on_voir()
        load_pourquoi_python()
 





            


