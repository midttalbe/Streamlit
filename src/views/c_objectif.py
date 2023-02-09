import streamlit as st
from src.views.components import side_bar

button_name = ["Source du Dataset","Contexte du Dataset","Colonnes du Dataset"]

def load_objectif():
    st.title("Objectif de l'analyse")
    
    st.markdown("""
        Le dataset permet de visualiser pour chaque ligne une réservation ou bien une annulation de réservation pour des établissements hôteliers.
    """)

def load_source_jeu_donnees():
    st.header("""
    Source du jeu de données 
    """)
    st.markdown("""
    Le jeu de données provient du site internet Kaggle qui regroupe plusieurs sources de données ouvert à tous :

    https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand

    La version utilisée dans notre analyse est la version 1.

    Le fichier source est au format CSV avec séparateur de virgule.
    """)
def load_contexte():
    st.header("""
            Contexte du dataset :
            """)
    st.markdown("""
        Notre jeu de données couvre une **période de 4 ans** allant de 2014 à 2017. 

        Il contient environ **120 000 lignes**.

        Cet ensemble de données contient des informations de réservation pour un hôtel de ville et un hôtel de villégiature, ainsi que des informations telles que la date de la réservation, la durée du séjour, le nombre d’adultes, d’enfants et / ou de bébés et le nombre de places de parking disponibles, entre autres.

        Toutes les informations d’identification personnelle ont été supprimées des données.


    """)

def load_colonnes():
    st.header("""
    Liste des colonnes du dataset :
    """)
    st.write("Notre jeu de données contient en tout 32 colonnes qui sont détaillées ci-dessous.")
    with st.container():
        st.markdown("""
        > 01. **'hotel' (String)** : \n
                type d'hôtel {'City Hotel','Resort Hotel'}.
        """)
        st.markdown("""
        > 02. **'is_canceled' (Bool)** : \n
                Valeur indiquant si la réservation a été annulée (1) ou non (0).
                """)
        st.markdown("""
        > 03. **'lead_time' (Integer)** : \n
                Nombre de jours qui se sont écoulés entre la date de saisie de la réservation dans le PMS et la date d'arrivée.
                """)
        st.markdown("""
        > 04. **'arrival_date_year' (Integer)** : \n
                Année d'arrivée.
        """)
        st.markdown("""
        > 05. **'arrival_date_month' (String)** : \n
                Mois d’arrivée, exemple : Juillet, Août, ... .
                """)
        st.markdown("""        
        > 06. **'arrival_date_week_number' (Integer)** : \n
                Numéro de semaine d'arrivée.
                """)
        st.markdown(""" 
        > 07. **'arrival_date_day_of_month' (Integer)** : \n
                Jour d'arrivée.
                """)
        st.markdown("""
        > 08. **'stays_in_weekend_nights' (Integer)** : \n
                Nombre de nuités en week-end (samedi ou dimanche) où le client a séjourné ou réservé pour séjourner à l'hôtel.
                """)
        st.markdown("""
        > 09. **'stays_in_week_nights' (Integer)** : \n
                Nombre de nuités en semaine (du lundi au vendredi) où le client a séjourné ou réservé pour séjourner à l'hôtel.
                """)
        st.markdown("""        
        > 10. **'adults' (Integer)** :  \n
            Nombre d'adultes.
                """)
        st.markdown("""
        > 11. **'children' (Integer)** : \n
            Nombre d'enfants.
            """)

        st.markdown("""
        > 12. **'babies' (Integer)** : \n
            Nombre de bébés.
            """)

        st.markdown("""
        > 13. **'meal' (String)** : \n
            Type de repas réservé. Les catégories sont présentées dans des forfaits repas d'accueil standard. 
            """)

        st.markdown("""
        > 14. **'country' (String)** : \n
            Pays d'origine. Les catégories sont représentées au format ISO 3155-3:2013, exemple : PRT, GBR, ... .
            """)

        st.markdown("""
        > 15. **'market_segment' (String)** : \n 
            Désignation du segment de marché.
            """) 

        st.markdown("""
        > 16. **'distribution_channel' (String)** : \n
            Canal de distribution de réservation.
            """)

        st.markdown("""
        > 17. **'is_repeated_guest' (Bool)** : \n
            Valeur indiquant si le nom de la réservation provient d'un client répété (1) ou non (0).
            """)

        st.markdown("""
        > 18. **'previous_cancellations' (Integer)** : \n
            Nombre de réservations précédentes qui ont été annulées par le client avant la réservation en cours.
            """)

        st.markdown("""
        > 19. **'previous_bookings_not_canceled' (Integer)** : \n
            Nombre de réservations précédentes non annulées par le client avant la réservation en cours.
            """)

        st.markdown("""
        > 20. **'reserved_room_type' (String)** : \n
            Code du type de chambre réservé. Le code est présenté au lieu d’une désignation pour des raisons d’anonymat.
            """)

        st.markdown("""
        > 21. **'assigned_room_type' (String)** : 
            Code pour le type de chambre attribué à la réservation.
            Parfois le type de chambre assigné différe de celui reservé à cause d'opérations diverses effectuées par l'hotel (ex: overbooking) ou bien par le client.
            Le code est affiché uniquement pour des raisons d'anonynimisation.""")

        st.markdown("""        
        > 22. **'booking_changes' (Integer)** : \n
            Nombre de changements/modifications apportés à la réservation depuis le moment où la réservation a été saisie dans le PMS jusqu'au moment de l'enregistrement ou de l'annulation.
                """)
        
        st.markdown("""
        > 23. **'deposit_type' (String)** : \n
            Indique si le client a effectué un dépôt pour garantir la réservation. 
            Cette variable peut prendre trois catégories : 
                - No Deposit - aucun dépôt n'a été effectué ; 
                - Non Refund - un dépôt a été effectué avec une valeur égale au coût total du séjour ; 
                - Refundable - un dépôt a été effectué avec une valeur inférieure au coût total du séjour.
                    """)
        
        st.markdown("""
        > 24. **'agent'** : \n
            pas utile
            """)

        st.markdown("""
        > 25. **'company'** :\n 
            pas utile
            """)

        st.markdown("""
        > 26. **'days_in_waiting_list'** :\n 
            Nombre de jours où la réservation est restée sur la liste d'attente avant d'être confirmée au client.
            """)

        st.markdown("""
        > 27. **'customer_type'** : \n
            Type de réservation, en assumant l'une des quatre catégories suivantes :
                - Contract - lorsque la réservation est associée à un allotissement ou à un autre type de contrat. 
                - Group - lorsque la réservation est associée à un groupe. 
                - Transient - lorsque la réservation ne fait pas partie d'un groupe ou d'un contrat, et n'est pas associée à une autre réservation transitoire.
                - Transient-party - lorsque la réservation est transitoire, mais qu'elle est associée à au moins une autre réservation transitoire.
        """)

        st.markdown("""
        > 28. **'adr'** :
            Le tarif journalier moyen est défini en divisant la somme de toutes les transactions d'hébergement par le nombre total de nuits d'hébergement. 
            Explication : Inclure le prix total de toutes les transactions d'hébergement, y compris le prix de la chambre, sur le nombre de nuits pour obtenir un prix moyen par nuit.
        """)

        st.markdown("""
        > 29. **'required_car_parking_spaces'** :
            Nombre d'emplacements de parking requis par le client.
            """)

        st.markdown("""
        > 30. **'total_of_special_requests'** : 
            Nombre de demandes spéciales faites par le client (par exemple, lit double ou étage élevé).
            """)
        
        st.markdown("""
        > 31. **'reservation_status'** : 
            Dernier statut de la réservation, supposant l'une des trois catégories suivantes :
                - Canceled - la réservation a été annulée par le client ;
                - Check-Out - le client s'est enregistré mais a déjà quitté l'hôtel ; 
                - No-Show - le client ne s'est pas enregistré et a informé l'hôtel de la raison de son absence.
        """
        )
        
        st.markdown("""
        > 32. **'reservation_status_date'** : 
            Date à laquelle le dernier statut a été défini. 
            Cette variable peut être utilisée conjointement avec ReservationStatus pour savoir quand la réservation a été annulée 
            ou quand le client a quitté l'hôtel. 
            """)






def load_view():
    col_a,col_b,col_c = st.columns([1,4,1])
    with col_b:
        side_bar.load_sidebar()

        load_objectif()

        tab1, tab2, tab3 = st.tabs(["Source du jeu de données","Contexte du jeu de données","Colonnes du jeu de données"])

        with tab1:
            load_source_jeu_donnees()

        with tab2:
            load_contexte()

        with tab3:    
            load_colonnes()
