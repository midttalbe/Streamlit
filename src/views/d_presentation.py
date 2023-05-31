import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
# from src.router import redirect
# from src.controllers import auth as c_auth
from src.views.components import side_bar
from src.controllers.analyse import Analyse

# à reconfigurer dans le fichier .streamlit/config.toml 
# [deprecation]
# showPyplotGlobalUse = false


def load_view():
    col_a,col_b,col_c = st.columns([1,4,1])
    with col_b:
        side_bar.load_sidebar()

        st.title("Présentation détaillée des colonnes du jeu de données")

        st.set_option('deprecation.showPyplotGlobalUse', False) 
        # st.markdown("# Le dataset est détaillé ci-dessous : ")

        st.subheader("Présentation des 5 premières lignes du dataset :")
        # df = pd.read_csv(r'C:\Backup\Documents_PERSO\Formations_Datarockstars\Projet DATA\DATA\hotel_bookings\hotel_bookings.csv')
        st.markdown("""<br>""",unsafe_allow_html=True)
        a = Analyse()
        a.read(False)
        df = a.getDF() #.loc[:,"booking_id":"reservation_status_date"]
        # Insertion d'un identifiant unique pour chaque ligne de réservation
        df.insert(0,'booking_id',df.reset_index().index + 1)
        
        st.table(df.head(5))

        col_list  = df.columns.to_list()
        col_list.sort()
        st.subheader("Veuillez selectionner une colonne du jeu de données pour afficher sa distribution")
        st.markdown("""<br>""",unsafe_allow_html=True)
        option = st.selectbox('Veuillez selectionner une colonne pour afficher la distribution', col_list,label_visibility="collapsed")
        map_mois = {"January":["Janvier",1], "February":["Février",2], "March":["Mars",3], "April":["Avril",4], "May":["Mai",5], "June":["Juin",6]
                ,"July":["Juillet",7], "August":["Août",8], "September":["Septembre",9], "October":["Octobre",10], "November":["Novembre",11], "December":["Décembre",12]}

        
        if option == "hotel":
            st.write("""<h4><strong>Distribution des types d'hotel : </h4></strong""",unsafe_allow_html=True)
            # fig = plt.figure(figsize=(3,3))
            df_graph = df['hotel'].value_counts().rename("Type d'hôtel")
            st.bar_chart(df_graph)

        elif option == "is_canceled" :
            st.subheader("Distribution du statut de la réservation : ")
            df_graph = df['is_canceled'].value_counts().rename("Réservation/Annulation").replace().reset_index()
            df_graph['type'] = df_graph['index'].map(lambda x: "Réservation" if x == 0 else "Annulation")
            del df_graph['index']
            st.bar_chart(df_graph.set_index("type"))

        elif option == "lead_time":
            fig = plt.figure(figsize=(3,3))
            st.subheader("Distribution du lead time : ")
            g = sns.displot(df,x='lead_time',kind='hist',height=4,color='blue',aspect=2)
            st.pyplot(g)

        elif option == "arrival_date_year":
            fig = plt.figure(figsize=(6,3))
            st.subheader("Distribution de l'année d'arrivée dans l'hotel : ")
            sns.countplot(x=df['arrival_date_year'],color='blue')
            st.pyplot(fig)

        elif option == "arrival_date_month":
            fig = plt.figure(figsize=(5,3))
            st.subheader("Distribution du mois d'arrivée dans l'hotel : ")
            df_graph = df.groupby('arrival_date_month')["booking_id"].count().rename("Nb").reset_index()
            df_graph["Mois,Num"] = df_graph["arrival_date_month"].map(map_mois)
            df_graph["Mois"] = df_graph["Mois,Num"].apply(lambda x:x[0])
            df_graph["Num"] = df_graph["Mois,Num"].apply(lambda x:x[1])
            df_graph.sort_values(by="Num",inplace=True)
            sns.barplot(df_graph,y='Mois',x="Nb",color='blue')
            st.pyplot(fig)

        elif option == "arrival_date_week_number":
            fig = plt.figure(figsize=(10,5))
            st.subheader("Distribution de la semaine d'arrivée dans l'hotel : ")
            g = sns.countplot(x=df['arrival_date_week_number'],color='blue')
            g.tick_params(axis='x', rotation=90)
            g
            st.pyplot(fig)

        elif option == "arrival_date_day_of_month":
            fig = plt.figure()
            st.subheader("Distribution du jour d'arrivée dans l'hotel : ")
            sns.countplot(df,y='arrival_date_day_of_month',color='blue')
            st.pyplot(fig)

        elif option == "stays_in_weekend_nights":
            fig = plt.figure(figsize=(12,5))
            st.subheader("Distribution du nombre de nuits en weekend passé à l'hotel : ")
            sns.countplot(df,y='stays_in_weekend_nights',color='blue')
            st.pyplot(fig)

        elif option == "stays_in_week_nights":
            fig = plt.figure(figsize=(9,6))
            st.subheader("Distribution du nombre de nuits en semaine passé à l'hotel : ")
            sns.countplot(df,y='stays_in_week_nights',color='blue')
            st.pyplot(fig)

        elif option == "adults":
            fig = plt.figure(figsize=(12,5))
            st.subheader("Distribution du nombre d'adultes ayant séjournés à l'hotel : ")
            sns.countplot(df,y='adults',color='blue')
            st.pyplot(fig)

        elif option == "children":
            fig = plt.figure(figsize=(12,5))
            st.subheader("Distribution du nombre d'enfants ayant séjournés à l'hotel : ")
            sns.countplot(y=df['children'].fillna('NA'),color='blue',order=df['children'].fillna('NA').value_counts(ascending=False).index)
            st.pyplot(fig)

        elif option == "babies":
            fig = plt.figure(figsize=(12,5))
            st.subheader("Distribution du nombre de bébé ayant séjournés à l'hotel : ")
            sns.countplot(y=df['babies'],color='blue')
            st.pyplot(fig)

        elif option == "meal":
            fig = plt.figure(figsize=(12,5))
            st.subheader("Distribution de la formule repas choisie : ")
            sns.countplot(y=df['meal'],color='blue')
            st.pyplot(fig)
            st.markdown("""
            > Explications des différents termes :
                - BB - Bed & Breakfast : Petit Déjeuner uniquement
                - HB - Half board : Petit Déjeuner avec Déjeuner ou Diner
                - FB - Full board : Formule tout compris
                - Undefined/SC : Aucune formule de repas choisie  
            """)

        elif option == "country":
            df1 = df['country'].value_counts().reset_index().head(9)
            country_list = df1['index'].unique()

            def grp_country_top(country):
                if country in country_list:
                    return country
                else:
                    return 'Others'

            df2 = df['country'].map(grp_country_top).value_counts().reset_index()
            df2.rename(columns={'index':'Country','country':'Nb values'},inplace=True)
            st.subheader("TOP 10 de la distribution du pays d'origine du client :")

            # col1, col2 = st.columns([8,5])
            # with col1:
            fig1, ax1 = plt.subplots()
            # fig1.set_size_inches(5,3)
            ax1.pie(df2['Nb values'],labels=df2['Country'],autopct='%1.01f%%',explode=[0.05]*10)
            st.pyplot(fig1)

        elif option == "market_segment":
            fig = plt.figure(figsize=(12,6))
            st.subheader("Distribution de la colonne segment marketing :")
            sns.countplot(y=df['market_segment'],color='blue')
            st.pyplot(fig)
            st.markdown("""
            >
                - “TA” pour “Travel Agents”  
                - “TO” pour “Tour Operators”
            """
            )

        elif option == "distribution_channel":
            fig = plt.figure(figsize=(12,6))
            st.subheader("Répartition de la colonne canal de distribution :")
            sns.countplot(y=df['distribution_channel'],color='blue')
            st.pyplot(fig)
            st.markdown("""
            >
                - “TA” pour “Travel Agents”  
                - “TO” pour “Tour Operators”
            """
            )  

        elif option == "is_repeated_guest":
            fig = plt.figure(figsize=(12,6))
            sns.countplot(x=df['is_repeated_guest'],color='blue')
            st.subheader("Client régulier ou nouveau client :")
            st.pyplot(fig)
            st.markdown("""
            >
                - 0 si nouveau client  
                - 1 si client régulier
            """
            )  

        elif option == "previous_cancellations":
            fig = plt.figure(figsize=(12,6))
            sns.countplot(x=df['previous_cancellations'],color='blue')
            st.subheader("Nombre de réservations précédentes annulées par le client avant la réservation en cours :")
            st.pyplot(fig)

        elif option == "previous_bookings_not_canceled":
            fig = plt.figure(figsize=(3,3))
            g = sns.displot(x=df['previous_bookings_not_canceled'],color='blue',kind='hist',height=5,aspect=1.5)
            st.subheader("Nombre de réservations précédentes non annulées par le client avant la réservation en cours :")
            st.pyplot(g)

        elif option == "reserved_room_type":
            fig = plt.figure(figsize=(12,6))
            sns.countplot(x=df['reserved_room_type'].sort_values(ascending=True),color='blue')
            st.markdown(
            """
                >Code du type de chambre réservé :
            """)
            st.pyplot(fig)
            st.markdown(
            """>
                Le code est présenté au lieu de la désignation pour des raisons d'anonymat.
            """)

        elif option == "assigned_room_type":
            fig = plt.figure(figsize=(12,6))
            sns.countplot(x=df['assigned_room_type'].sort_values(ascending=True),color='blue')
            st.markdown(
            """        
                >Code pour le type de chambre attribué : 
            """)
            st.pyplot(fig)
            st.markdown(
            """>     
            Parfois, le type de chambre attribué diffère du type de chambre réservé pour des raisons de fonctionnement de l'hôtel (par exemple, surréservation) ou à la demande du client. 
        Le code est présenté au lieu d’une désignation pour des raisons d'anonymat.
            """)

        elif option == "booking_changes":
            fig = plt.figure(figsize=(12,6))
            sns.countplot(x=df['booking_changes'],color='blue')
            st.markdown(
            """        
                >Nombre de modifications/modifications apportées à la réservation : 
            """)
            st.pyplot(fig)
            st.markdown(
            """>
            à partir du moment où la réservation a été saisie sur le PMS jusqu'au moment de l'enregistrement ou de l'annulation
            """)

        elif option == "deposit_type":
            fig = plt.figure(figsize=(12,6))
            st.markdown(
            """        
                >Indication si le client a effectué un acompte pour garantir la réservation : 
            """)
            sns.countplot(x=df['deposit_type'].sort_values(),color='blue')
            st.pyplot(fig)
            st.markdown(
            """>
            Cette variable peut assumer trois catégories : 
            - No Deposit : aucun dépôt n'a été effectué
            - Non refund : un acompte a été effectué d'une valeur du coût total du séjour  
            - Refundable : un acompte a été effectué avec une valeur inférieure au coût total du séjour
            """)

        elif option == "days_in_waiting_list":
            fig = plt.figure(figsize=(3,3))
            st.markdown(
            """        
                >Nombre de jours pendant lesquels la réservation était dans la liste d’attente avant d’être confirmée au client :
            """)
            g = sns.displot(df,x='days_in_waiting_list',kind='hist',color='blue',height=5,aspect=2)
            st.pyplot(g)

        elif option == "customer_type":
            fig = plt.figure(figsize=(12,6))
            st.markdown(
            """        
                >Type de réservation :
            """)
            sns.countplot(x=df['customer_type'].sort_values(),color='blue')
            st.pyplot(fig)
            st.markdown(
            """>
            Détail des quatres catégories :
        - Contrat : lorsque la réservation est associée à une attribution ou à un autre type de contrat
        - Groupe : lorsque la réservation est associée à un groupe
        - Transitoire : lorsque la réservation ne fait pas partie d'un groupe ou d'un contrat, et n'est pas associée à une autre réservation temporaire
        - Partie transitoire : lorsque la réservation est transitoire, mais est associée à au moins une autre réservation transitoire     
            """)

        elif option == "adr":
            fig = plt.figure(figsize=(3,3))
            st.markdown(
            """        
                >Tarif journalier moyen (adr) : défini en divisant la somme de toutes les transactions d'hébergement par le nombre total de nuitées :
            """) 
            df_adr = df[df['adr']<1000]
            g = sns.displot(data=df_adr,x='adr',height=5,aspect=2)
            st.pyplot(g)

        elif option == "required_car_parking_spaces":
            fig = plt.figure(figsize=(12,6))
            st.markdown(
            """        
                >Nombre de places de parking demandées par le client :
            """)   
            sns.countplot(x=df['required_car_parking_spaces'],color='blue')
            st.pyplot(fig)

        elif option == "total_of_special_requests":
            fig = plt.figure(figsize=(12,6))
            st.markdown(
            """        
                >Nombre de demandes spéciales faites par le client (par exemple, lit double ou étage élevé) :
            """) 
            sns.countplot(x=df['total_of_special_requests'],color='blue')
            st.pyplot(fig)

        elif option == "reservation_status":
            fig = plt.figure(figsize=(12,6))
            st.markdown(
            """        
                >Réservation dernier statut :
            """)
            sns.countplot(x=df['reservation_status'],color='blue')
            st.pyplot(fig)
            st.markdown(
            """>
            - Annulée : la réservation a été annulée par le client
        - Check-Out : le client s'est enregistré mais est déjà parti
        - No-Show : le client ne s'est pas enregistré et a informé l'hôtel de la raison   
            """)

        elif option == "reservation_status_date":
            fig = plt.figure(figsize=(12,6))
            st.markdown(
            """        
                >Date à laquelle le dernier statut a été défini : 
            """)
            col = pd.to_datetime(df['reservation_status_date'])
            g = sns.displot(col,kind='hist', color='blue',height=5,aspect=2)
            g.tick_params(axis='x', rotation=90)
            st.pyplot(g)
            st.markdown(
            """>
            Cette variable peut être utilisée conjointement avec le statut de réservation pour comprendre :
            - quand la réservation a été annulée 
            - ou quand le client a-t-il quitté l'hôtel
            """)

