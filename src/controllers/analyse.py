from src.models.datalake import Datalake
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np

class Analyse():

    def __init__(self) -> None:
        self.df_dict = {} #datalake().getDataframe()
        self.datalake = Datalake()


    def load(self):
        self.datalake.load()

    def read(self):
        self.df_dict = self.datalake.getDataframe()
        self.global_transform()

    def getDF(self):
        return self.df_dict["df"]

    def getDFbooked_date(self):
        return self.df_dict["df_booked_date"]

    def getDFresult_grouped(self):
        return self.df_dict["result_grouped"]
        
    def global_transform(self):
        df = self.getDF()
        df.insert(0,'booking_id',df.reset_index().index + 1)

        # Suppression des colonnes agent et company
        drop_column = ['agent','company']
        for col in df.columns:
            if col in drop_column:
                df.drop(col,axis=1,inplace=True)

        map_month = {'January':"1", 'February':"2", 'March':"3", 'April':"4", 'May':"5", 'June':"6",
                    'July':"7", 'August':"8", 'September':"9", 'October':"10", 'November':"11", 'December':"12"}

        # Ajout d'une colonne calculé 'arrival_date_month_number' derivé de la colonne 'arrival_date_month'
        df['arrival_date_month_number'] = df['arrival_date_month'].map(map_month)

        # Ajout d'une colonne de type date arrival_date
        df['arrival_date'] = df['arrival_date_year'].astype('string') + '-' + df['arrival_date_month_number'] + '-' + df['arrival_date_day_of_month'].astype('string')
        df['arrival_date'] = pd.to_datetime(df['arrival_date']) 

        # Convert la colonne reservation_status_date en datetime
        df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'])

        # Check nb nuité
        df['Nb_total_nuit'] = df['reservation_status_date'] - df['arrival_date']
        df['Nb_total_nuit'] = df['Nb_total_nuit'].dt.days
        df['stays_total'] = df['stays_in_week_nights'] + df['stays_in_weekend_nights']

        # Ajout colonne departure_date = arrival_date + nb_stays pour les lignes not canceled
        df['departure_date'] = df['arrival_date'] + pd.to_timedelta(df['stays_total'], unit='D')
        df['departure_date'] = pd.to_datetime(df['departure_date'])

        # Remplace les valeurs NA dans la colonne "children" par 0
        df["children"] = df['children'].fillna(0)

        # Ajout du nombre total de personne 
        df['total_client'] = df['adults'] + df['children'] + df['babies']

        # Créer un dataframe avec les reservations confirmées 
        df_booked = df.loc[df['is_canceled']==0]

        # Unpivot date range et split rows de la date range from arrival_date to departure_date
        df_booked = df_booked.loc[:,['arrival_date','departure_date','booking_id']]

        # MAJ df df_booked
        self.df_dict["df"] = df

        # create result dataframe
        df_booked_date = self.getDFbooked_date()
        result = pd.merge(df_booked_date,df[['booking_id','total_client','stays_total']],on='booking_id')
        result_grouped = result.groupby(["Date","Year","Quarter","Week Number","Month Number","Month Name","Day of Month","Day Name","Day Number","Day Type"])['total_client'].sum().reset_index()

        # Ajoute result_grouped dans le dictionnaire de DF
        self.df_dict["result_grouped"] = result_grouped

    # def getData(self):
    #     return self.df 

    # Analyse 1 : par mois et par années
    def analyse_1_1(self, année:int):
        ###########################
        # Préparation des données #
        ###########################
        result_grouped = self.getDFresult_grouped()
        result_grouped_month_year = result_grouped.groupby([result_grouped["Year"],result_grouped["Quarter"], result_grouped["Month Number"],result_grouped["Month Name"]])['total_client'].mean().reset_index()

        ###########################
        # Visualisation graphique #
        ###########################

        dict_color = {0:"black",2015:"blue",2016:"orange",2017:"green"}
        highlight_color = 'red'
        highlight_label = 'Minimum'
        color = dict_color[année]

        # Creating legend with color box
        red_patch = mpatches.Patch(color=highlight_color, label=highlight_label)

        if année != 0:

            # Graphique Bar par années
            df_graph = result_grouped_month_year[result_grouped_month_year['Year'] == année]
            
            min_value = df_graph['total_client'].min()
            df_graph['Min in red'] = df_graph['total_client'] == min_value
            
            fig, ax = plt.subplots(1,1,figsize=(6,4))

            sns.barplot(data=df_graph,x='Month Name',y='total_client',hue='Min in red',palette=[color,highlight_color],dodge=False)

            plt.title('Moyenne de fréquentation en répartition par mois pour l\'année ' + str(année) + "\n")
            plt.legend(handles=[red_patch])
            plt.xticks(rotation = 90)
            return fig

        else:
            # Graphique Bar pour toutes les années
            fig, ax = plt.subplots(1,1,figsize=(6,4))

            df_graph = result_grouped_month_year.groupby(["Month Number","Month Name"])["total_client"].mean().reset_index()
            min_value = df_graph["total_client"].min()
            df_graph["Min in red"] = df_graph["total_client"] == min_value
            sns.barplot(data=df_graph,x='Month Name',y='total_client',hue='Min in red',palette=[color,highlight_color],dodge=False)
            plt.title("Moyenne de fréquentation en répartition par mois toutes années confondues\n")
            plt.legend(handles=[red_patch])
            plt.xticks(rotation = 90)

            return fig