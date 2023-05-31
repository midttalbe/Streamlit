import streamlit as st
from  src.controllers import auth as c_auth
from src.views.components import side_bar

def load_view():
    
    col_a,col_b,col_c = st.columns([1,4,1])

    with col_b:
        side_bar.load_sidebar()
        
        st.title("Conclusions")
        st.markdown("""
        Nous avons pu voir la mise en place d'un site applicatif dédié à des analyses de données.<br>
        Ce site est donc capable de <b>répondre entièrement aux questionnements de départ.</b><br>

        Il est :<br>
        <ul>
        <li>Responsive</li>
        <li>Interactif</li>
        <li>Disponible à un large public</li>
        <li>Sécurisé par connexion</li>
        </ul>

        Il existe plusieurs <b>pistes d'amélioration</b> :<br>
        <ul>
        <li>Ajouter plus d'interactivité : laisser la possibilité d'effectuer des commentaires ou d'ajouter des notes</li>
        <li>Permettre à l'utilisateur d'enregistrer des préférences en termes de couleurs ou de critère de sélection de données</li>
        <li>Ajout d'un vrai section « Admin » pour la gestion des utilisateurs</li>
        <li>Ajout d'un log de suivi des interactions utilisateurs effectuées sur le site : pour des statistiques d'usage par exemple</li>
        </ul>

        Pour aller encore plus loin, il serait possible d'effectuer du <b>« Machine Learning »</b> car le jeu de données s'y prête bien.<br>
        En effet, on a à notre disposition des lignes de réservation et des lignes d'annulation.<br>

        Il serait donc possible d'effectuer du training sur ce jeu de données afin de pouvoir <b>profiler les clients qui sont le plus susceptible d'annuler un réservation</b> en fonction de plusieurs critères :<br>
        <ul>
        <li>Le client est déjà connu</li>
        <li>Le client a effectué un certain nombre de modification de réservation</li>
        <li>Le client a réservé tant de jour avant le début du séjour à l'hôtel</li>
        </ul>
        """,unsafe_allow_html=True)