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


    def load(self,forced:bool=False):
        self.datalake.load(forced)

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

    # Analyse 1 - 1 : par mois et par années
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
            
            fig, ax = plt.subplots(1,1,figsize=(5,3))

            sns.barplot(data=df_graph,x='Month Name',y='total_client',hue='Min in red',palette=[color,highlight_color],dodge=False)

            plt.title('Moyenne de fréquentation en répartition par mois pour l\'année ' + str(année) + "\n")
            plt.legend(handles=[red_patch])
            plt.xlabel("Mois")
            plt.ylabel("Fréquentation client")
            plt.xticks(rotation = 90)
            return fig

        else:
            # Graphique Bar pour toutes les années
            fig, ax = plt.subplots(1,1,figsize=(5,3))

            df_graph = result_grouped_month_year.groupby(["Month Number","Month Name"])["total_client"].mean().reset_index()
            min_value = df_graph["total_client"].min()
            df_graph["Min in red"] = df_graph["total_client"] == min_value
            sns.barplot(data=df_graph,x='Month Name',y='total_client',hue='Min in red',palette=[color,highlight_color],dodge=False)
            plt.title("Moyenne de fréquentation en répartition par mois toutes années confondues\n")
            plt.legend(handles=[red_patch])
            plt.xlabel("Mois")
            plt.ylabel("Fréquentation client")
            plt.xticks(rotation = 90)

            return fig

    # Analyse 1 - 2 : Distribution par semestre et par mois toutes années confondues
    def analyse_1_2(self,semestre:int):
        ###########################
        # Préparation des données #
        ###########################
        result_grouped = self.getDFresult_grouped()
        result_grouped_month_year = result_grouped.groupby([result_grouped["Year"],result_grouped["Quarter"], result_grouped["Month Number"],result_grouped["Month Name"]])['total_client'].mean().reset_index()
        ## Group by Quarter for all years
        df_graph_box = result_grouped_month_year[['Quarter','Month Number','Month Name','total_client']]

        ###########################
        # Visualisation graphique #
        ###########################

        semesters = [[1, 2], [3, 4]]
        semester = semesters[semestre]
        df_graph_box = result_grouped_month_year[['Quarter','Month Number','Month Name','total_client']]
        df_graph_box.sort_values(by='Month Number',inplace=True)
        df_graph_box_sem = df_graph_box[df_graph_box["Quarter"].isin(semester)]
        
        sem = int(np.ceil(semester[0]/2))
        fig, ax = plt.subplots(1,1,figsize=(6,4))
        sns.boxplot(df_graph_box_sem,x='Month Name',y="total_client")

        plt.xticks(rotation = 90)
        plt.xlabel("Mois")
        plt.ylabel("Fréquentation client")
        plt.title("Distribution de fréquentation pour le semester n°" + str(sem) + " répartie par mois toutes années confondues")

        return fig

    # Analyse 1 - 3 : Par rapport au numéro du jour dans le mois par années - Graphique en Camember
    def analyse_1_3(self, année:int):
        ###########################
        # Préparation des données #
        ###########################

        explode_distance = 0.3

        def cutDayOfMonth(daynum):
            if daynum <= 5: return '01-05'
            elif daynum <= 10: return '06-10'
            elif daynum <= 15: return '11-15'
            elif daynum <= 20: return '16-20'
            elif daynum <= 25: return '21-25'
            else: return '> 25'

        result_grouped = self.getDFresult_grouped()

        result_grouped_day_of_month = result_grouped.groupby([result_grouped["Year"],result_grouped["Day of Month"]])['total_client'].sum().reset_index()
        result_grouped_day_of_month['grpDay'] = result_grouped_day_of_month['Day of Month'].apply(cutDayOfMonth)
        result_grouped_day_of_month = result_grouped_day_of_month.groupby(['Year','grpDay'])['total_client'].mean().rename('total_client_mean').reset_index()
        result_grouped_day_of_month['rank'] = result_grouped_day_of_month.groupby(['Year'])['total_client_mean'].rank()

        ###########################
        # Visualisation graphique #
        ###########################

        if année != 0:
            # Graphique Pie Chart par année
            year = année
            
            df_graph_pie_day_of_month = result_grouped_day_of_month[result_grouped_day_of_month['Year'] == year]
            rank_list = df_graph_pie_day_of_month['rank']
            f = lambda x : explode_distance if x == 1 else 0.05
            explode_list = list(map(f,rank_list)) 
            
            fig, ax = plt.subplots(1,1,figsize=(5,5))

            plt.pie(df_graph_pie_day_of_month['total_client_mean'],labels=df_graph_pie_day_of_month['grpDay'],autopct='%1.0f%%',explode=explode_list,shadow = True)
            plt.title("Moyenne de fréquentation par rapport au numéro du jour dans le mois pour l'année " + str(year) + "\n")
            plt.legend(title="Numéro du jour",bbox_to_anchor=(0,0.7))
            
            return fig

        else:
            # Graphique Pie Chart toutes années 
            df_graph_pie_day_of_month = result_grouped_day_of_month.groupby("grpDay")["total_client_mean"].mean().reset_index()
            df_graph_pie_day_of_month['rank'] = df_graph_pie_day_of_month['total_client_mean'].rank()
            rank_list = df_graph_pie_day_of_month['rank']
            f = lambda x : explode_distance if x == 1 else 0.05
            explode_list = list(map(f,rank_list)) 

            fig, ax = plt.subplots(1,1,figsize=(5,5))

            plt.pie(df_graph_pie_day_of_month['total_client_mean'],labels=df_graph_pie_day_of_month['grpDay'],autopct='%1.0f%%',explode=explode_list,shadow = True)
            plt.title("Moyenne de fréquentation par rapport au numéro du jour dans le mois toutes années confondues\n")
            plt.legend(title="Numéro du jour",bbox_to_anchor=(0,0.7))

            return fig
