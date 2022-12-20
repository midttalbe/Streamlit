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
                type d'hôtel {'City Hotel','Resort Hotel'}
        """)
        st.markdown("""
        > 02. **'is_canceled' (Bool)** : \n
                Value indicating if the booking was canceled (1) or not (0)
                """)
        st.markdown("""
        > 03. **'lead_time' (Integer)** : \n
                Number of days that elapsed between the entering date of the booking into the PMS and the arrival date.
                """)
        st.markdown("""
        > 04. **'arrival_date_year' (Integer)** : \n
                Year of arrival date
        """)
        st.markdown("""
        > 05. **'arrival_date_month' (String)** : \n
                Month of arrival date, exemple : July, August
                """)
        st.markdown("""        
        > 06. **'arrival_date_week_number' (Integer)** : \n
                Week number of year for arrival date.
                """)
        st.markdown(""" 
        > 07. **'arrival_date_day_of_month' (Integer)** : \n
                Day of arrival date
                """)
        st.markdown("""
        > 08. **'stays_in_weekend_nights' (Integer)** : \n
                Number of weekend nights (Saturday or Sunday) the guest stayed or booked to stay at the hotel
                """)
        st.markdown("""
        > 09. **'stays_in_week_nights' (Integer)** : \n
                Number of week nights (Monday to Friday) the guest stayed or booked to stay at the hotel
                """)
        st.markdown("""        
        > 10. **'adults' (Integer)** :  \n
            Number of adults
                """)
        st.markdown("""
        > 11. **'children' (Integer)** : \n
            Number of children
            """)

        st.markdown("""
        > 12. **'babies' (Integer)** : \n
            Number of babies
            """)

        st.markdown("""
        > 13. **'meal' (String)** : \n
            Type of meal booked. Categories are presented in standard hospitality meal packages: 
            """)

        st.markdown("""
        > 14. **'country' (String)** : \n
            Country of origin. Categories are represented in the ISO 3155–3:2013 format, example: PRT, GBR
            """)

        st.markdown("""
        > 15. **'market_segment' (String)** : \n 
            Market segment designation.
            """) 

        st.markdown("""
        > 16. **'distribution_channel' (String)** : \n
            Booking distribution channel.
            """)

        st.markdown("""
        > 17. **'is_repeated_guest' (Bool)** : \n
            Value indicating if the booking name was from a repeated guest (1) or not (0)
            """)

        st.markdown("""
        > 18. **'previous_cancellations' (Integer)** : \n
            Number of previous bookings that were cancelled by the customer prior to the current booking
            """)

        st.markdown("""
        > 19. **'previous_bookings_not_canceled' (Integer)** : \n
            Number of previous bookings not cancelled by the customer prior to the current booking
            """)

        st.markdown("""
        > 20. **'reserved_room_type' (String)** : \n
            Code of room type reserved. Code is presented instead of designation for anonymity reasons.
            """)

        st.markdown("""
        > 21. **'assigned_room_type' (String)** : 
            Code for the type of room assigned to the booking.
            Sometimes the assigned room type differs from the reserved room type due to hotel operation reasons (e.g. overbooking) or by customer request.
            Code is presented instead of designation for anonymity reasons.""")

        st.markdown("""        
        > 22. **'booking_changes' (Integer)** : \n
            Number of changes/amendments made to the booking from the moment the booking was entered on the PMS until the moment of check-in or cancellation
                """)
        
        st.markdown("""
        > 23. **'deposit_type' (String)** : \n
            Indication on if the customer made a deposit to guarantee the booking. 
            This variable can assume three categories: 
                - No Deposit - no deposit was made; 
                - Non Refund - a deposit was made in the value of the total stay cost; 
                - Refundable - a deposit was made with a value under the total cost of stay.
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
            Number of days the booking was in the waiting list before it was confirmed to the customer
            """)

        st.markdown("""
        > 27. **'customer_type'** : \n
            Type of booking, assuming one of four categories:
                - Contract - when the booking has an allotment or other type of contract associated to it 
                - Group – when the booking is associated to a group 
                - Transient – when the booking is not part of a group or contract, and is not associated to other transient booking
                - Transient-party – when the booking is transient, but is associated to at least other transient booking
        """)

        st.markdown("""
        > 28. **'adr'** :
            Average Daily Rate as defined by dividing the sum of all lodging transactions by the total number of staying nights. 
            Explications : inclus le prix total de toutes les préstations incluant le prix de la chambre sur le nombre de nuits pour avoir un prix moyen par nuité.
        """)

        st.markdown("""
        > 29. **'required_car_parking_spaces'** :
            Number of car parking spaces required by the customer
            """)

        st.markdown("""
        > 30. **'total_of_special_requests'** : 
            Number of special requests made by the customer (e.g. twin bed or high floor)
            """)
        
        st.markdown("""
        > 31. **'reservation_status'** : 
            Reservation last status, assuming one of three categories:
                - Canceled - booking was canceled by the customer;
                - Check-Out - customer has checked in but already departed; 
                - No-Show - customer did not check-in and did inform the hotel of the reason why
        """
        )
        
        st.markdown("""
        > 32. **'reservation_status_date'** : 
            Date at which the last status was set. 
            This variable can be used in conjunction with the ReservationStatus to understand when was the booking canceled 
                or when did the customer checked-out of the hotel.
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
