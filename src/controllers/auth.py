from src.models import database as conn, cookie as ck
import hashlib as hash

def hash_pass(password:str):
    hashed_password = hash.sha256(password.encode("utf-8")).hexdigest()
    return(hashed_password)

# Permet d'inscrire un nouvel utilisateur en base de données
# Paramètre d'entrée : name (nom d'utilisateur), email (login), password (mot de passe en clair)
# Retour : True si l'utilisateur a été correctement crée en base de données, False sinon
def signin(name, email, password):
    hashed_password = hash_pass(password)
    db = conn.Database()
    if db.is_user_already_exists(email):
        return False
    try:
        db.create_new_user(name, email, hashed_password)
        return True
    except:
        return False

# Permet de vérifier si le login et le mot de passe corresponde bien à ce que se situe en base de données
# Paramètre d'entrée : login (texte), password (texte)
# Retour : booléen True si l'authentification est correcte, False si l'authentification a echouée
def authentification(login, password):
    # Connexion au modèle base de données contenant les informations de connexion des utilisateurs enregistré sur le site
    db = conn.Database()
    
    # Convertion du mot de passe clair en ligne de hachage pour vérificatoin
    hashed_pass = hash_pass(password)

    # Requête de selection des données de la base de données sur la table USERS
    verify_login = f"SELECT uid, name, email FROM users WHERE email=?"
    verify_password = f"SELECT uid, name, email FROM users WHERE password=?"

    # Execute les requêtes SQL
    res_login = db.execute(verify_login,(login,)).fetchall()
    res_password = db.execute(verify_password,(hashed_pass,)).fetchall()
    
    # Récupère et teste le résultat
    res = set(res_login).intersection(set(res_password))
 
    # Si le resultat est OK : on créer un cookie de connexion
    # Sinon la fonction renvoie la valeur False indiquant que la connexion a echouée
    if res:
        # print(res)
        key = ['uid', 'name', 'email']
        js = dict(zip(key, list(*res)))
        ck.Cookie().ecrire(js)
        return True
    else:
        return False

def isAuthenticated():
    js = ck.Cookie().lire()

    if js and js['uid']:
        return True
    else:
        return False

def getUserName():
    js = ck.Cookie().lire()
    if js:
        return js['name']
    else:
        return "No name"

def deconnexion():
    ck.Cookie().drop()



# def authentification2(login, password):
#     db = conn.Database()
#     verify_login = f"SELECT * FROM users WHERE email=%s AND password=%s"
    
#     res = db.cursor_execute(verify_login,(login,password))
        
#     if res:
#         return True
#     else:
#         return False