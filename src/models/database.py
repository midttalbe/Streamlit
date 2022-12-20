import sqlite3 as sql
# import pandas as pd
import hashlib as hash

class Database():

    def __init__(self, _db:str="Projet.sqlite"):
        self.db_con = sql.connect(_db)
        self.execute = self.db_con.execute
        self.commit = self.db_con.commit

    def hash_pass(self, password:str):
        hashed_password = hash.sha256(password.encode("utf-8")).hexdigest()
        return(hashed_password)

    def connect(self):
        return self.db_con

    def is_user_already_exists(self, email):
        try:
            res = self.execute(f"SELECT count(*) FROM users WHERE email='{email}'")
            nb_found = res.fetchone()[0]
            if nb_found > 0:
                return True
            else:
                return False
        except:
            return True

    def create_new_user(self, name, email, hashed_password):
        try:
            self.execute(f"INSERT INTO users(email, name, password) VALUES ('{email}','{name}','{hashed_password}')")
            self.commit()
            return True
        except:
            return False

    def setup(self):
        self.drop()
        self.execute("CREATE TABLE users(uid INTEGER PRIMARY KEY, email VARCHAR, name VARCHAR, password VARCHAR)")
        self.commit()
        name, email, admin_hashed_pass = "Admin","admin@datarockstars.ai",self.hash_pass("password")
        self.execute(f"INSERT INTO users(name, email, password) VALUES ('{name}','{email}','{admin_hashed_pass}')")
        self.commit()
        print("Setup is finished !")

    def drop(self,table_name=['users']):
        list_table = table_name
        for table in list_table :
            drop_query = "DROP TABLE IF EXISTS " + table
            self.execute(drop_query)
            self.commit()

    def importCSV(url:str):
        pass

    def execute(self,_q:str):
        return self.db_con.execute(_q)

    def getAllTables(self):
        q = """SELECT 
                    name
               FROM 
                    sqlite_schema
               WHERE 
                    type ="table" AND 
                    name NOT LIKE "sqlite_%";"""
        return [ele[0] for ele in self.execute(q).fetchall()]

    def table_exists(self, table_name:str):
        return table_name in self.getAllTables()

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