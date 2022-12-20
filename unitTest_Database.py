import unittest
from src.models.database import Database

class UnitTest(unittest.TestCase):

    def test_execute(self):
        schema_query = "SELECT count(*) FROM sqlite_schema"

        # Create Database object
        db = Database()

        # Execute schema query
        res = db.execute(schema_query).fetchone()

        # Test if schema db is readable if not connection there is a connection issue
        self.assertNotEqual(res[0],0,"La connexion à la base de données a echoué !")

    def test_insert(self):
        insert_query = "INSERT INTO users(email, password) VALUES ('email@email.com', 'password')"
        select_query = "SELECT count(*) FROM users WHERE email = 'email@email.com'"

        # Create Database object
        db = Database()

        # Insert users email@email.com
        db.execute(insert_query)

        # Read table users and get the count of user email@email.com 
        res = db.execute(select_query).fetchone()[0]

        # test if user email@email.com is correctly inserted into users table
        self.assertNotEqual(res,0,"Insert users test email@email.com failed !")

    def test_delete(self):
        """
        Test Delete
        """
        delete_query = "DELETE FROM users WHERE email='email@email.com'"
        select_query = "SELECT count(*) FROM users WHERE email = 'email@email.com'"

        # Create Database object
        db = Database()

        # Delete users email@email.com
        db.execute(delete_query)

        # Read table users and get the count of user email@email.com 
        res = db.execute(select_query).fetchone()[0]

        self.shortDescription()
        # test if user email@email.com is correcty deleted from users table 
        self.assertEqual(res,0,"Delete users test email@email.com failed !")

if __name__ == "__main__":
    unittest.main()

