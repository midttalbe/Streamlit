import json

class Cookie:

    def __init__(self):
        pass

    def lire(self):
        with open('cookie.json', mode="r") as file:
            return (json.load(file))
        
    def ecrire(self, data):
        with open('cookie.json', mode='w') as file:
            json.dump(data, file, indent=True)

    def clean(self):
        c = self.lire()
        keys = c.keys()
        for key in keys:
            c[key] = None
        self.ecrire(c)

    def update(self, data):
        c = self.lire()
        keys = data.keys()
        for key in keys:
            c[key] = data[key]
        self.ecrire(c)

    def drop(self):
        self.ecrire({})


