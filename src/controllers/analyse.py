from src.models.datalake import Datalake
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import squarify as sqry

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
        
    def getDFresult_country(self):
        return self.df_dict["result_country"]

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

        # Pour les analyses 2
        # Récupère les colonnes country et nombre de client
        result_country = pd.merge(df_booked_date,df[['booking_id','country','total_client','stays_total']],on='booking_id')     
        self.df_dict["result_country"] = result_country

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

    # Analyse 1 - 4 : Par rapport au jour de la semaine pour toutes les années - Grapqhique en Cluster
    def analyse_1_4(self,type_de_graph:str):
        ###########################
        # Préparation des données #
        ###########################

        result_grouped = self.getDFresult_grouped()
        explode_distance = 0.3

        # Par rapport au jour de la semaine 
        result_grouped_day_of_week = result_grouped.groupby([result_grouped["Year"],result_grouped["Week Number"],result_grouped["Day Type"],result_grouped["Day Number"], result_grouped["Day Name"]])["total_client"].sum().reset_index()

        if type_de_graph == "CLUSTER":
            #############################
            # Visualisation graphique 1 #
            ############################# 

            fig, ax = plt.subplots(1,1,figsize=(6,3))

            df_graph_square = result_grouped_day_of_week.groupby('Day Type')['total_client'].mean().reset_index()
            sqry.plot(sizes=df_graph_square['total_client'],label=df_graph_square['Day Type'],alpha=0.7,pad=1,color=sns.color_palette("Spectral",2))

            return fig

        else:
            #############################
            # Visualisation graphique 2 #
            ############################# 

            df_graph_pie_day_of_week = result_grouped_day_of_week.groupby(["Day Number","Day Name"])["total_client"].mean().reset_index()
            df_graph_pie_day_of_week['rank'] = df_graph_pie_day_of_week["total_client"].rank()
            rank_list = df_graph_pie_day_of_week['rank']
            f = lambda x : explode_distance if x == 1 else 0.05
            explode_list = list(map(f,rank_list)) 

            fig, ax = plt.subplots(1,1,figsize=(4,4))

            plt.title("Moyenne de fréquentation par rapport au jour de la semaine toutes années confondues\n\n")
            plt.pie(df_graph_pie_day_of_week["total_client"],labels=df_graph_pie_day_of_week["Day Name"],autopct='%1.0f%%',explode=explode_list,shadow = True)       
            
            return fig


    # Analyse 2 - 1 : Distribution du nombre de pays representé par mois et par année
    def analyse_2_1(self,année:int):
        ###########################
        # Préparation des données #
        ###########################

        # Récupère les colonnes country et nombre de client
        result_country = self.getDFresult_country()
        result_country_grouped_year_month = result_country.groupby([result_country["Year"],result_country["Month Number"],result_country["Month Name"]])['country'].nunique().rename('Nb Pays Unique').reset_index()

        ###########################
        # Visualisation graphique #
        ###########################

        highlight_label = "Maximum"
        dict_color = {0:"black",2015:"blue",2016:"orange",2017:"green"}
        highlight_color = 'red'
        color = dict_color[année]

        # Creating legend with color box
        red_patch = mpatches.Patch(color=highlight_color, label=highlight_label)

        # Counting nombre de country unique par année et par mois
        year = année

        if year != 0:
            
            df_graph_country = result_country_grouped_year_month[result_country_grouped_year_month["Year"] == year]
            max_value = df_graph_country["Nb Pays Unique"].max()
            df_graph_country["Max in red"] = df_graph_country["Nb Pays Unique"] == max_value

            fig, ax = plt.subplots(1,1,figsize=(5,3))

            sns.barplot(data=df_graph_country,x="Month Name",y="Nb Pays Unique",dodge=False,hue="Max in red",palette=[color, highlight_color])
            plt.title("Nombre total de pays uniques representés par mois pour l'année " + str(year))
            plt.legend(handles=[red_patch])
            plt.xticks(rotation = 90)
            ax.set_xlabel("Mois")
            return fig

        else:
            # Graphique Bar pour toutes les années
            df_graph_country = result_country_grouped_year_month.groupby(["Month Number","Month Name"])["Nb Pays Unique"].mean().reset_index()
            max_value = df_graph_country["Nb Pays Unique"].max()
            df_graph_country["Max in red"] = df_graph_country["Nb Pays Unique"] == max_value

            fig, ax = plt.subplots(1,1,figsize=(5,3))

            sns.barplot(data=df_graph_country,x="Month Name",y="Nb Pays Unique",dodge=False,hue="Max in red",palette=["black", highlight_color])
            plt.title("Nombre total de pays uniques representés par mois toutes années confondues\n")
            plt.legend(handles=[red_patch])
            plt.xticks(rotation = 90)
            ax.set_xlabel("Mois")

            return fig


    # Analyse 2 - 2 : TOP 3 des pays les plus representés selon le mois de l'années
    def analyse_2_2(self, année:int):
        ###########################
        # Préparation des données #
        ###########################

        # Most represented country for each month of year
        result_country = self.getDFresult_country()
        result_country_grouped = result_country.groupby(["Year","country","Month Number","Month Name","Day of Month"])['total_client'].sum().rename("total_client_sum").reset_index()
        result_country_grouped = result_country_grouped.groupby(['Year',"country","Month Number","Month Name"])['total_client_sum'].mean().rename('total_client_mean').reset_index()

        # Création de la palette de couleur pour chaque pays top 3 de l'année
        top = 3
        country_top_list = []
        list_year = [2015, 2016, 2017]
        color_list = ["blue","green","red","yellow","purple","orange"]
        for i in range(len(list_year)):
            year = list_year[i]
            df_country= result_country_grouped[result_country_grouped["Year"] == year]
            df_country["rank"] = df_country.groupby(["Month Number", "Month Name"])["total_client_mean"].rank(ascending=False,method="dense")
            df_country_top = df_country[df_country["rank"] <= top]
            country_top_list.extend(df_country_top['country'].unique())

        country_top_list = pd.Series(country_top_list).unique()
        country_color_dict = dict(zip(country_top_list,color_list))

        ###########################
        # Visualisation graphique #
        ###########################

        year = année

        if year != 0:

            # TOP Country Hotel Frequentation by Month for each year 2015, 2016, 2017
            df_graph_hist = result_country_grouped[result_country_grouped["Year"] == year]
            df_graph_hist.sort_values(["Month Number", "Month Name", "total_client_mean"],inplace=True)
            df_graph_hist["rank"] = df_graph_hist.groupby(["Month Number", "Month Name"])["total_client_mean"].rank(ascending=False,method="dense")
            df_top = df_graph_hist[df_graph_hist["rank"] <= top]

            fig, ax = plt.subplots(1,1,figsize=(5,3))

            g = sns.histplot(df_top,x="Month Name",hue="country",weights="total_client_mean",multiple="stack",legend=True,palette=country_color_dict) #,stat="percent"
            plt.title("Top " + str(top) + " Moyenne de fréquentation journalière par Pays par Mois pour l'année " + str(year) + "\n")
            plt.xticks(rotation = 90)
            ax.set_xlabel("Mois")
            ax.set_ylabel("Fréquentation client")
            legend = ax.get_legend()
            legend.set_title("Pays")
            legend.set_bbox_to_anchor((-0.15, 0.5))

            return fig

        else:
            # TOP Country Hotel Frequentation by Month for all years
            df_graph_hist_all = result_country_grouped.groupby(["Month Number","Month Name","country"])["total_client_mean"].mean().reset_index()
            df_graph_hist_all["rank"] = df_graph_hist_all.groupby(["Month Number", "Month Name"])["total_client_mean"].rank(ascending=False,method="dense")
            df_top_all = df_graph_hist_all[df_graph_hist_all["rank"] <= top]

            fig, ax = plt.subplots(1,1,figsize=(5,3))

            sns.histplot(df_top_all,x="Month Name",hue="country",weights="total_client_mean",multiple="stack",legend=True,palette=country_color_dict) #,stat="percent"
            plt.title("Top " + str(top) + " Moyenne de fréquentation journalière par Pays par Mois pour toutes les années\n")
            plt.xticks(rotation = 90)
            
            ax.set_xlabel("Mois")
            ax.set_ylabel("Fréquentation client")

            legend = ax.get_legend()
            legend.set_title("Pays")
            legend.set_bbox_to_anchor((-0.15, 0.5))

            return fig
