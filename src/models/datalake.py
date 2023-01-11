from src.models.csv import CSV
from src.models.database import Database
import pandas as pd

class Datalake():
    def __init__(self) -> None:
        self.pathDF = "src/assets/hotel_bookings.csv"
        self.pathDFbooked = "src/assets/df_booked_date.csv"
        self.sql_hotel_booking = "Hotel_Booking"
        self.sql_booked_date = "Booked_Date"

    def load(self,forced_in_db:bool=False):
        self.df = CSV().readCSV(self.pathDF)
        self.df_booked_date = CSV().readCSV(self.pathDFbooked)
        self.store_in_DB(forced_in_db)


    def store_in_DB(self,forced:bool=False):
        db = Database()
        if(forced or not db.table_exists(self.sql_hotel_booking)):
            with db.db_con as conn:
                self.df.to_sql(name=self.sql_hotel_booking,con= conn,if_exists="replace",index=False)
                db.commit()
        
        if(forced or not db.table_exists(self.sql_booked_date)):
            with db.db_con as conn:
                self.df_booked_date.to_sql(name=self.sql_booked_date, con=conn,if_exists="replace",index=False)
                db.commit()

    def getDataframe(self):
        db = Database()
        with db.db_con as conn:
            df = pd.read_sql("SELECT * FROM Hotel_Booking",conn)
            df_booked_date = pd.read_sql("SELECT * FROM Booked_Date",conn)
        self.df_dict = { "df":df, "df_booked_date":df_booked_date }
        return self.df_dict

    
datalk = Datalake()
datalk.load(True)