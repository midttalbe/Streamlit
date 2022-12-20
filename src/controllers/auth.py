from src.models import database as conn, cookie as ck
import hashlib as hash

def hash_pass(password:str):
    hashed_password = hash.sha256(password.encode("utf-8")).hexdigest()
    return(hashed_password)

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

def authentification(login, password):
    db = conn.Database()
    # verify_login = f"SELECT * FROM users WHERE email='{login}' AND password='{password}'"
    
    hashed_pass = hash_pass(password)

    verify_login = f"SELECT uid, name, email FROM users WHERE email='{login}'"
    verify_password = f"SELECT uid, name, email FROM users WHERE password='{hashed_pass}'"

    res_login = db.execute(verify_login).fetchall()
    res_password = db.execute(verify_password).fetchall()
    
    res = set(res_login).intersection(set(res_password))
 
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