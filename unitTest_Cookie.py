import unittest
from src.models.cookie import Cookie

class UnitTest(unittest.TestCase):

    def test_clean(self):
        
        c = Cookie()
        c.clean()
        cookie = c.lire()
        nb_nonvide = 0
        keys = cookie.keys()
        for key in keys:
            if cookie[key] != None:
                nb_nonvide +=1
                break;

        self.assertEqual(nb_nonvide,0,"Le Clean Cookie n'a pas fonctionné !")


    def test_drop(self):

        c = Cookie()
        c.drop()

        self.assertEqual(c.lire(),{},"Le Drop Cookie n'a pas fonctionné !")

    
    def test_update(self):
        test_cookie = {"test_clé":"0"}
        c = Cookie()
        c.update(test_cookie)
        cookie = c.lire()
        try:
            test_value = cookie["test_clé"]
            self.assertEqual(test_value,"0","L'Update Cookie n'a pas fonctionné !")
        except KeyError:
            self.fail()
        finally:
            c.drop()



if __name__ == "__main__":
    unittest.main()