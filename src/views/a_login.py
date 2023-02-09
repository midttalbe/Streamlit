import streamlit as st
from  src.controllers import auth as c_auth
from PIL import Image
import re
from src.router import redirect

# Permet de vérifier que l'email est au format correct ceci à l'aide d'une expression régulière
# Paramètre d'entré : email (login de l'utilisateur)
# Retour : True si l'email est au bon format, False sinon
def check(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

def check_password(pass1, pass2):
    if pass1 == pass2:
        return True
    else:
        return False

# Affiche le formulaire de connexion au site internet
# Paramètre d'entrée : image (binary image)
# Paramètre de sortie : aucun
def load_login_form(image):
    # affiche l'image du formulaire
    st.image(image, channels="RGB", output_format="auto")

    # affiche le formulaire
    with st.form("login_form",clear_on_submit=True):   
        st.write("Veuillez entrer vos informations de connexion :")
        login = st.text_input("Login :",value="admin@datarockstars.ai")
        password = st.text_input("Mot de passe : ", type="password", value="password")
        res = st.form_submit_button(label="Login")
        # test si le login est conforme (bon format email) et qu'il n'est pas vide
        if login and check(login):
            if res:
                # appel du controller de vérification du couple Login et Mot de passe
                # si retour OK : alors redirige l'u
                # tilisateur vers la page d'accueil du site
                # sinon : affichage d'un message d'erreur et la redirection vers la page d'accueil ne s'effectue pas 
                if c_auth.authentification(login, password):
                    st.success("Authenfication correct")
                    redirect("/b_home",reload=True)
                else:
                    st.error("Problème d'authenfication !")
        else:
            if login != None:
                st.error("Nom d'utilisateur ou mot de passe incorrect !")


# Affiche le formulaire d'inscription utilisateur
# Paramètre d'entrée : aucun
# Retour : 
def load_signin_form():

    with st.expander("Si vous n'avez pas encore de compte, veuillez completer le formulaire ci-dessous : ",expanded=True):
        # Affiche le formulaire
        with st.form("signin_form"):
            # Affiche les champs de saisie
            st.write("Formulaire d'inscription :")
            name = st.text_input("Nom :", value="")
            email = st.text_input("Email :", value="")
            password1 = st.text_input("Mot de passe : ", type="password", value="")
            password2 = st.text_input("Saisissez à nouveau votre mot de passe : ", type="password", value="")
            res2 = st.form_submit_button(label="S'inscrire")

            # Vérification des saisies
            if res2:

                error_count = 0

                # Vérification si nom d'utilisateur est vide
                if name == "":
                    st.error("Le nom n'est pas renseigné")
                    error_count += 1

                # Vérrification si email est vide
                if email == "":
                    st.error("Le mail n'est pas renseigné")
                    error_count += 1

                # Vérification si le premier champ de saisie du mot de passe est vide
                if password1 == "":
                    st.error("Le mot de passe est vide")
                    error_count += 1

                # Vérification si le mot de passe 1 est identique au mot de passe 2
                if not check_password(password1,password2):
                    st.error("Les mots de passe ne correspondent pas")
                    error_count += 1

                # Vérification si email est au format correct
                if not check(email):
                    st.error("Le format de l'adresse mail est incorrect")
                    error_count += 1                       

                # Si erreur affiche un message d'erreur
                # Sinon poursuit le processus d'inscription du nouvel utilisateur
                if error_count == 0:
                    # Vérifie si l'utilisateur n'existe pas déjà en base de données
                    if c_auth.signin(name, email, password1):
                        st.success(f"Inscription terminé l'utilisateur {email} a été crée")
                        c_auth.authentification(email, password1)
                        redirect("/b_home",reload=True)
                    else:
                        st.error(f"Problème lors de l'inscription : l'utilisateur {email} existe déjà !")  
                        return False 

def _max_width_():
    max_width_str = f'max-width: 500px';

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


def load_view():

    image = Image.open("src/images/image_booking.jpg")

    # Login
    col8, col7, col6 = st.columns([1,4,1])
    with col8:
        st.empty()

    with col7:
        _max_width_()
        load_login_form(image)
        load_signin_form()        
                
    with col6:
        st.empty()