# import sqlite3 as sql
import pandas as pd

class CSV():
    
    def __init__(self) -> None:
        pass

    def readCSV(self,path):
        return pd.read_csv(path)

    def writeCSV(self):
        pass
