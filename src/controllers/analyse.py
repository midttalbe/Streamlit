from src.models.datalake import Datalake
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import squarify as sqry
from matplotlib.lines import Line2D


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

    def getDFresult_client_category(self):
        return self.df_dict["result_client_category"]

    def getDFdf_prix(self):
        return self.df_dict["df_prix"]

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

        #######################
        # Pour les analyses 2 #
        #######################

        # Récupère les colonnes country et nombre de client
        result_country = pd.merge(df_booked_date,df[['booking_id','country','total_client','stays_total']],on='booking_id')     
        self.df_dict["result_country"] = result_country

        #######################
        # Pour les analyses 3 #
        #######################

        # Création des catégories selon les critères suivants :
        def procRow_Categorie(row):
            nbAdult = row["adults"]
            nbChildren = row["children"]
            nbBabies = row["babies"]

            if (nbBabies + nbChildren) > 0 :
                if nbAdult == 2:
                    return ["Avec Enfants","Couple"]
                elif nbAdult == 1:
                    return ["Avec Enfants","Personne seule"]
                elif nbAdult > 2:
                    return ["Avec Enfants","Groupe"]
                elif nbAdult == 0:
                    return ["Avec Enfants", "Enfants non accompagnés"]
                else:
                    return ["Avec Enfants", "None"]

            else:
                if nbAdult == 2:
                    return ["Sans Enfants","Couple"]
                elif nbAdult == 1:
                    return ["Sans Enfants","Personne seule"]
                elif nbAdult > 2:
                    return ["Sans Enfants","Groupe"]
                else:
                    return ["Sans Enfants", "None"]

        col_client_category = ["booking_id","adults","children","babies","total_client"]
        # col_df = ["booking_id","Date","adults","children","babies","total_client"]
        # Merge avec le df global pour récuperer les colonnes 'adults','children','babies','total_client'

        tmp_df = df.loc[df['is_canceled']==0][col_client_category]
        tmp_df = tmp_df[tmp_df["total_client"] >0]

        # Création de la catégorie client
        tmp_df["Client Category 2"] = tmp_df.apply(procRow_Categorie,axis=1)

        # MAJ des champs 'Client Category','Client Subcategory'
        tmp_df["Client Category"] = tmp_df["Client Category 2"].apply(lambda x:x[0])
        tmp_df["Client Subcategory"] = tmp_df["Client Category 2"].apply(lambda x:x[1])

        result_client_category = pd.merge(tmp_df,df_booked_date,on="booking_id")

        del tmp_df

        self.df_dict["result_client_category"] = result_client_category

        #######################
        # Pour les analyses 4 #
        #######################

        # Préparation des données pour le calcul de prix le plus bas

        # Si assigned room est égale à reserved room alors 0
        # Si assigned room est supérieur à reserved room alors 1
        # Si assigned room est infèrieur à reserved room alors -1
        def calculate_surclassement(row):
            assigned = row['assigned_room_type']
            reserved = row['reserved_room_type']

            if assigned < reserved: return 1
            else: return 0

        def calculate_declassement(row):
            assigned = row['assigned_room_type']
            reserved = row['reserved_room_type']

            if assigned > reserved: return 1
            else: return 0

        # Filtre colonne adr > 0 et total_client > 0
        col = ['booking_id','hotel','assigned_room_type','reserved_room_type','stays_total','adults','children','total_client','adr','is_repeated_guest','meal']
        df_tmp = df[col][(df['adr'] > 0) & (df['total_client'] > 0)]
        df_tmp['adr_client'] = (df_tmp['adr'])/ (df_tmp['total_client'])
        df_tmp['is_surclassement'] = df_tmp.apply(calculate_surclassement, axis=1)
        df_tmp['is_declassement']  = df_tmp.apply(calculate_declassement, axis=1)
        df_tmp['is_regular'] = df_tmp['assigned_room_type'] == df_tmp['reserved_room_type']
        df_tmp['is_regular'] = df_tmp['is_regular'].apply(int)

        df_prix = pd.merge(df_booked_date,df_tmp,on='booking_id')
        self.df_dict["df_prix"] = df_prix
        del df_tmp        


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
        fig, ax = plt.subplots(1,1,figsize=(7,5))
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

        def change_width(ax, new_value) :
            for patch in ax.patches :
                current_width = patch.get_width()
                diff = current_width - new_value

                # we change the bar width
                patch.set_width(new_value)

                # we recenter the bar
                patch.set_x(patch.get_x() + diff * .5)

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

            change_width(ax, .85)

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

            change_width(ax, .85)

            return fig


    # Analyse 3 - 1 : Par catégorie client et par mois et années
    def analyse_3_1(self, année:int):
        result_client_category = self.getDFresult_client_category()

        ###########################
        # Préparation des données #
        ###########################

        # Calcul de la moyenne par jour du nombre de personne par catégorie
        result_client_category_grouped = result_client_category.groupby(["Year","Client Category","Month Number","Month Name","Day of Month"])["booking_id"].count().rename("Count Category").reset_index()
        result_client_category_grouped = result_client_category_grouped.groupby(["Year","Client Category","Month Number","Month Name"])["Count Category"].mean().rename("Avg Count Category").reset_index()

        ###########################
        # Visualisation graphique #
        ###########################

        color_cat = ["lightblue","lightgreen"]
        pal_cat = dict(zip(result_client_category_grouped["Client Category"].unique(),color_cat))

        year = année

        def change_width(ax, new_value) :
            for patch in ax.patches :
                current_width = patch.get_width()
                diff = current_width - new_value

                # we change the bar width
                patch.set_width(new_value)

                # we recenter the bar
                patch.set_x(patch.get_x() + diff * .5)

        if year != 0:
            # Graphique repartition des categories de client par Mois et par Année
            df_graph_cat = result_client_category_grouped[result_client_category_grouped["Year"] == year]

            fig, ax = plt.subplots(1,1,figsize=(5,4))
            
            g = sns.histplot(df_graph_cat,x="Month Name",weights="Avg Count Category",hue="Client Category",stat="percent",multiple="stack",palette=pal_cat)
            g.legend(title="Catégorie Client",labels=["Sans Enfants","Avec Enfants"],loc='upper left',bbox_to_anchor=(1,1))
            plt.title("Moyenne des réservations en % par catégorie client par mois pour l'année " + str(year) +"\n")
            plt.xticks(rotation = 90)

            ax.set_xlabel("Mois")
            ax.set_ylabel("% Réservations")

            change_width(ax, .85)

            return fig

        else:
            # Graphique global repartition des categories de client par Mois pour toutes les années 
            df_graph_cat_all = result_client_category_grouped.groupby(["Month Number","Month Name","Client Category"])["Avg Count Category"].mean().reset_index()

            fig, ax = plt.subplots(1,1,figsize=(5,3))

            g = sns.histplot(df_graph_cat_all,x="Month Name",weights="Avg Count Category",hue="Client Category",stat="percent",multiple="stack",palette=pal_cat)
            g.legend(title="Catégorie Client",labels=["Sans Enfants","Avec Enfants"],loc='upper left',bbox_to_anchor=(1,1))
            plt.title("Moyenne des réservations en % par catégorie client par mois pour toutes les années\n")
            plt.xticks(rotation = 90)

            ax.set_xlabel("Mois")
            ax.set_ylabel("% Réservations")

            change_width(ax, .85)

            return fig


    # Analyse 3 - 2 : Par sous catégorie de client - grahique polaire 
    def analyse_3_2(self):
        ###########################
        # Préparation des données #
        ###########################

        result_client_category = self.getDFresult_client_category()

        # Group by Category and Sub Category of Client 
        result_client_subcategory_grouped = result_client_category.groupby(["Year","Client Category","Client Subcategory","Month Number","Month Name","Day of Month"])["booking_id"].count().rename("Count Category").reset_index()
        result_client_subcategory_grouped = result_client_subcategory_grouped.groupby(["Year","Client Category","Client Subcategory","Month Number","Month Name"])["Count Category"].mean().rename("Avg Count Category").reset_index()

        ######################################
        # Préparation des données graphiques #
        ######################################

        # Create dataframe for the polar chart
        df_polar = result_client_subcategory_grouped.groupby(["Month Number","Month Name","Client Category","Client Subcategory"])["Avg Count Category"].mean().reset_index()
        client_cats = ["Avec Enfants","Sans Enfants"]
        df_polars = [df_polar[df_polar["Client Category"] == client_cat] for client_cat in client_cats]
        bar_list = []
        label_list = []
        sub_cat_list = []
        # Calcule une dataframe qui somme toutes les sous catégories par mois
        df_polar_month_sums = [df_polar.groupby("Month Name")["Avg Count Category"].sum().rename("Sum Month").reset_index() for df_polar in df_polars]

        for i in range(len(df_polar_month_sums)):
            df_polar = df_polars[i]
            df_polar_month_sum = df_polar_month_sums[i]
            sub_df_list = []
            
            # boucle pour chaque sous catégorie on créer une liste de valeur qui va être consommé par le polar chart
            for subcategory in df_polar['Client Subcategory'].unique():
                sub_df = df_polar[df_polar["Client Subcategory"] == subcategory].groupby(["Month Number","Month Name"])["Avg Count Category"].mean().rename('Avg Count Subcategory').reset_index()
                
                # Calculate the percentage of each subcategory by total of all subcategory in the same month
                sub_df = pd.merge(sub_df,df_polar_month_sum,on='Month Name')
                
                # Calculate percentage in the month
                sub_df['Avg Count Subcategory %'] = (sub_df['Avg Count Subcategory'] / sub_df['Sum Month']) * 100
                sub_df_list.append(sub_df['Avg Count Subcategory %'].to_list())
                
            bar_list.append(sub_df_list)

            label_list.append(sub_df['Month Name'].to_list())
            sub_cat_list.append(df_polar['Client Subcategory'].unique())

        ###########################
        # Visualisation graphique #
        ###########################

        # Polar chart répartition en pourcentage du total des sous catégorie "Avec Enfants" et "Sans Enfants"
        n_points = 12
        # inner_radius = 1

        all_sub_cat = pd.DataFrame(sub_cat_list).melt()['value'].dropna().drop_duplicates().to_list()
        color = ['lightblue','lightgreen','red','orange']
        color_dict = dict(zip(all_sub_cat,color))

        x_max = 2*np.pi
        x_coords = np.linspace(0.0, x_max, n_points, endpoint=False)
        width = x_max / (n_points)

        fig_list = []

        for i in range(2):
            fig, ax = plt.subplots(1,1,figsize=(5,5))

            sub_cat = sub_cat_list[i]
            bar = bar_list[i]
            lab = label_list[i]
            bottom = np.array([0.0]*12)
            client_cat = client_cats[i]
            sub_cat.sort()
            for j in range(len(sub_cat)):   
                cat = sub_cat[j]
                col = color[j]

                ax = plt.subplot(111, polar=True)
                ax.set_theta_zero_location("N") # place Janvier en position 0°
                sub_bar = bar[j]

                plt.thetagrids(range(0, 360, int(360/12)), (lab))
                ax.bar(
                    x_coords,
                    sub_bar,
                    width=width,
                    bottom=bottom,#inner_radius,
                    color=color_dict[sub_cat[j]],
                    edgecolor="black",
                    linewidth=0.6,
                    align='center'
                )
                bottom += np.array(sub_bar)
            
            plt.title("% Moyenne de fréquentation pour la catégorie \"" + client_cat + "\" par mois pour toutes les années\n")  

            plt.legend(bbox_to_anchor=(1,0),title=client_cat, labels=sub_cat,loc="center left")         
            
            fig_list.append(fig)

        return fig_list

    
    # Analyse 4 - 1 : Heatmap répartition des surclassements, déclassements et des inchangés
    def analyse_4_1(self):
        ######################################
        # Préparation des données graphiques #
        ######################################

        def format_percent(val): 
            val = val * 100
            if val>0.1:
                return np.round(val)
            elif val>0.01:
                return np.round(val,1)
            else:
                return np.round(val, 2)

        color_declassement = 'red'
        color_surclassement = 'blue'
        color_nochange = 'green'
        legend_heat = [mpatches.Patch(color=color_surclassement, label="% Surclassement"),
                    mpatches.Patch(color=color_declassement, label="% Déclassement"),
                    mpatches.Patch(color=color_nochange, label="% Inchangée"),
                    
                    ]

        df_prix = self.getDFdf_prix()

        df_heat_surclassement = df_prix[df_prix['is_surclassement']>=0]
        total_surclassement = df_heat_surclassement['is_surclassement'].sum()
        df_heat_surclassement_cross = pd.crosstab(df_heat_surclassement['assigned_room_type'],df_heat_surclassement['reserved_room_type'],values=df_heat_surclassement['is_surclassement'],aggfunc='sum')
        df_heat_surclassement_cross = np.round( (df_heat_surclassement_cross /total_surclassement ) * 100,2) 
        df_heat_surclassement_cross.replace(0,np.NaN,inplace=True)

        df_heat_declassement = df_prix[df_prix['is_declassement']>=0]
        total_declassement = df_heat_declassement['is_declassement'].sum() 
        df_heat_declassement_cross = pd.crosstab(df_heat_declassement['assigned_room_type'],df_heat_declassement['reserved_room_type'],values=df_heat_declassement['is_declassement'],aggfunc='sum')
        df_heat_declassement_cross = np.round( (df_heat_declassement_cross / total_declassement) * 100,2) 
        df_heat_declassement_cross.replace(0,np.NaN,inplace=True)

        df_heat_nochange = df_prix[df_prix['is_regular']>=0]
        total_nochange = df_heat_nochange['is_regular'].sum()
        df_heat_nochange_cross = pd.crosstab(df_heat_nochange['assigned_room_type'],df_heat_nochange['reserved_room_type'],values=df_heat_nochange['is_regular'],aggfunc='sum')
        df_heat_nochange_cross = np.round( (df_heat_nochange_cross /total_nochange ) * 100,2) 
        df_heat_nochange_cross.replace(0,np.NaN,inplace=True)

        ###########################
        # Visualisation graphique #
        ###########################

        fig, ax = plt.subplots(1,1,figsize=(12,10))

        sns.heatmap(df_heat_surclassement_cross,cmap='Blues',annot=True,fmt='g',cbar_kws = dict(shrink= 0.5,use_gridspec=True,location="right"))
        sns.heatmap(df_heat_declassement_cross,cmap='Reds',annot=True,fmt='g',cbar_kws = dict(shrink= 0.5,use_gridspec=True,location="left"))
        g = sns.heatmap(df_heat_nochange_cross,cmap='Greens',annot=True,fmt='g',cbar_kws = dict(shrink= 0.7,use_gridspec=False,location="bottom"))

        for t in g.texts:
            if float(t.get_text())<1:
                t.set_text("< 1")#t.get_text().replace('-','')) #if the value is greater than 0.4 then I set the text 
            elif float(t.get_text())>10:
                t.set_text(str(int(np.round(float(t.get_text())))))
            else:
                t.set_text(t.get_text()) # if not it sets an empty text

        plt.title("Répartition en % de type de chambre en terme de surclassement, de déclassement et d'inchangée toutes périodes confondues\n")
        plt.legend(bbox_to_anchor =(-0.3, 1),handles=legend_heat,loc="upper center")
        g.set_yticklabels(g.get_yticklabels(), rotation=90)
        plt.xlabel('Chambre Reservée')
        plt.ylabel('Chambre Assignée',rotation=90,loc='center')

        return fig

    # Analyse 4 - 2 : Linechart distribution surclassement, déclassement et inchangés par mois toutes années confondus
    def analyse_4_2(self):
        
        ######################################
        # Préparation des données graphiques #
        ######################################

        # Préparation des données nombre de Surclassement et Déclassement par mois 
        cols = ['Date','Month Name','Month Number','is_surclassement','is_declassement','is_regular']

        df_prix = self.getDFdf_prix()

        # Calcul du dataframe du graphique
        df_surclassement = df_prix[cols]
        df_surclassement_month = df_surclassement.groupby(['Month Number','Month Name'])[['is_surclassement','is_declassement','is_regular']].sum().reset_index()

        # Calcul des totaux
        total_surclassement = df_prix[df_prix['is_surclassement']>=0]['is_surclassement'].sum()
        total_declassement = df_prix[df_prix['is_declassement']>=0]['is_declassement'].sum() 

        # Calcul de chaque mesures sur le total de l'année
        total_regular = df_surclassement_month["is_regular"].sum()
        df_surclassement_month['is_surclassement %'] = (df_surclassement_month['is_surclassement'] + 1) / (total_surclassement + 1) * 100
        df_surclassement_month['is_declassement %'] = (df_surclassement_month['is_declassement'] + 1) / (total_declassement + 1) * 100
        df_surclassement_month['is_regular %'] = (df_surclassement_month['is_regular'] + 1) / (total_regular + 1) * 100

        ###########################
        # Visualisation graphique #
        ###########################

        fig, ax = plt.subplots(1,1,figsize=(5,4))

        # Légende personnalisée
        legend_line = [mpatches.Patch(color=[0.80811509, 0.54506305, 0.53468464], label="% Déclassement" ),
                    Line2D([0], [0], color='blue', lw=4, label='% Surclassement'),
                    Line2D([0], [0], color='green', lw=4, label='% Inchangée')
                    ]

        sns.lineplot(df_surclassement_month,x='Month Name',y='is_surclassement %',color='blue',legend="auto")
        plt.xticks(rotation = 90)

        sns.lineplot(df_surclassement_month,x='Month Name',y='is_regular %',color='green')
        sns.barplot(df_surclassement_month,x='Month Name',y='is_declassement %',color='red',alpha=0.6)
        plt.xticks(rotation = 90)

        plt.legend(bbox_to_anchor =(-0.3, 1),handles=legend_line,loc="upper center")
        
        ax.set_ylabel("Pourcentage - %")
        ax.set_xlabel("Mois")

        return fig

