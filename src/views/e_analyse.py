import streamlit as st
# from  src.controllers import auth as c_auth
from src.views.components import side_bar
from src.controllers.analyse import Analyse

def load_problematique():
    st.subheader("La problèmatique :")

    st.markdown("""
    Ce jeu de données a été analysé selon la problématique suivante :

    Quel est le meilleur moment pour réserver une chambre d'hôtel selon ces 4 angles de vue : 
    1) Le meilleur moment pour être au calme avec le moins d'affluence possible
    2) Le meilleur moment pour avoir le plus de diversité en terme de pays représenté
    3) Le meilleur moment pour les voyages selon que l'on séjourne avec des enfants ou sans enfants
    4) Le meilleur moment pour bénéficier d'un sur-classement de type de chambre ou bien en terme de prix attractif 
    """)

def load_transformation():
    st.markdown("Pour pouvoir analyser correctement le jeu de données et répondre à la problématique, le jeu de données a subi des transformations qui sont décrites ci-dessous :")
    st.markdown("""
    - Suppression des colonnes "agent" et "company" car inutile dans notre analyse 
    - Ajout d'une colonne "arrival_date_month_number" qui converti le nom du mois en numéro de mois
    - 
    """)

def load_analyse_1():
    pass

def load_view():
    col_a,col_b,col_c = st.columns([1,4,1])
    with col_b:
        side_bar.load_sidebar()
        
        st.title("Analyse du dataset")
        load_problematique()

        st.subheader("La transformation de données")
        with st.expander("Liste des transformations globales :"):
            load_transformation()

        st.subheader("L'analyse :")
        with st.expander("Le meilleur moment pour être au calme avec le moins d'affluence possible"):
            load_analyse_1()

        with st.expander("Le meilleur moment pour avoir le plus de diversité en terme de pays représenté"):
            st.markdown("...")


        with st.expander("Le meilleur moment pour les voyages selon que l'on séjourne avec des enfants ou sans enfants"):
            st.markdown("...")


        with st.expander("Le meilleur moment pour bénéficier d'un sur-classement de type de chambre ou bien en terme de prix attractif "):
            st.markdown("...")

