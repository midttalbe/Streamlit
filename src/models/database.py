import sqlite3 as sql
# import pandas as pd
import hashlib as hash

# Classe Database
# Permet d'effectuer des echanges avec la base de données de l'application web
class Database():

    # Constructeur 
    # Initialise la chaîne de connexion à la base de donnée
    def __init__(self, _db:str="Projet.sqlite"):
        self.db_con = sql.connect(_db)
        self.execute = self.db_con.execute
        self.commit = self.db_con.commit

    # Permet de hash le mot de passe 
    # Paramètre d'entrée : password (mot de passe en clair)
    # Retour : retourne le mot de passe hash en SHA256
    def hash_pass(self, password:str):
        hashed_password = hash.sha256(password.encode("utf-8")).hexdigest()
        return(hashed_password)

    # Permet d'executer une requête SQL
    # Paramètre d'entrée : _q (requête SQL)
    # Retour : return le résultat de l'execution de la requête
    def execute(self,_q:str,_p):
        return self.db_con.execute(_q,_p)

    # Retourne le token de connexion à la base de données
    def connect(self):
        return self.db_con

    # Vérifie si un utilisateur existe déjà en base de données
    # Paramètre d'entrée : email (login de l'utilisateur)
    # Retour : True si l'utilisateur existe déjà, False si l'utilisateur n'existe pas en base de données
    def is_user_already_exists(self, email):
        try:
            res = self.execute(f"SELECT count(*) FROM users WHERE email=?",(email,))
            nb_found = res.fetchone()[0]
            if nb_found > 0:
                return True
            else:
                return False
        except:
            return True

    # Permet d'insérer un nouvel utilisateur en base de données
    # Paramètre d'entrée : name (nom d'utilisateur), email (login), hashed_password (mot de passe haché)
    # Retour : True si l'insertion a été correctement effectué, False sinon
    def create_new_user(self, name, email, hashed_password):
        try:
            self.execute(f"INSERT INTO users(email, name, password) VALUES (?,?,?)",(email,name,hashed_password))
            self.commit()
            return True
        except:
            return False

    # Permet d'initialiser les données de la base avec un utilisateur Admin
    # Retour : aucun
    def setup(self):
        self.drop()
        self.execute("CREATE TABLE users(uid INTEGER PRIMARY KEY, email VARCHAR, name VARCHAR, password VARCHAR)")
        self.commit()
        name, email, admin_hashed_pass = "Admin","admin@datarockstars.ai",self.hash_pass("password")
        self.execute(f"INSERT INTO users(name, email, password) VALUES (?,?,?)",(name,email,admin_hashed_pass))
        self.commit()
        print("Setup is finished !")

    # Permet de supprimer la table Users
    # Retour : aucun
    def drop(self,table_name=['users']):
        list_table = table_name
        for table in list_table :
            drop_query = "DROP TABLE IF EXISTS " + table
            self.execute(drop_query)
            self.commit()
   
 

    # Permet de voir toutes les tables présentes dans la base de données
    # Paramètre d'entrée : aucun
    # Retour : retourne la liste des tables présents en base de données
    def getAllTables(self):
        q = """SELECT 
                    name
               FROM 
                    sqlite_schema
               WHERE 
                    type ="table" AND 
                    name NOT LIKE "sqlite_%";"""
        return [ele[0] for ele in self.execute(q).fetchall()]

    # Permet de vérifier si une table existe déjà en base de données
    # Paramètre d'entrée : table_name (nom de la table)
    # Retour : True si la table existe déjà, False sinon
    def table_exists(self, table_name:str):
        return table_name in self.getAllTables()


    # def importCSV(url:str):
    #   pass

    # def cursor(self,q:str):
    #     return self.db_con.cursor()

    # def cursor_execute(self, q,param):
    #     with self.cursor() as cur:
    #         return cur.execute(q, param)


    # def commit(self):
    #     self.db_con.commit()

# db = Database()
# print(db.getAllTables())
# print(db.table_exists("users"))
# db.setup()
# print(db.execute("select * FROM Booked_Date LIMIT 1").fetchall())
# print(db.execute("select * FROM Hotel_Booking LIMIT 1").fetchall())
# print(db.execute("SELECT count(*) FROM users WHERE email='mohamed@datarockstars.ai'").fetchone()[0])

# db.drop(["Booked_Date","Hotel_Booking"])