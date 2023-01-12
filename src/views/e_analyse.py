import streamlit as st
# from  src.controllers import auth as c_auth
from src.views.components import side_bar
from src.controllers.analyse import Analyse

def load_problematique():
    st.subheader("La problèmatique :")

    st.markdown("""
    Ce jeu de données a été analysé selon la problématique suivante :

    Quel est le meilleur moment pour réserver une chambre d'hôtel selon ces 4 angles de vue : 
    1) Le meilleur moment pour être au calme avec le moins d'affluence possible
    2) Le meilleur moment pour avoir le plus de diversité en terme de pays représenté
    3) Le meilleur moment pour les voyages selon que l'on séjourne avec des enfants ou sans enfants
    4) Le meilleur moment pour bénéficier d'un sur-classement de type de chambre ou bien en terme de prix attractif 
    """)

def load_transformation():
    st.markdown("Pour pouvoir analyser correctement le jeu de données et répondre à la problématique, le jeu de données a subi des transformations qui sont décrites ci-dessous :")
    
    st.markdown("""
    - Suppression des colonnes "agent" et "company" car inutile dans notre analyse 
    """)
    with st.expander("Voir le code python :"):
        st.code("""
# Suppression des colonnes "agent" et "company"
drop_column = ['agent','company']
for col in df.columns:
    if col in drop_column:
        df.drop(col,axis=1,inplace=True)
        """)

    st.markdown("""
    - Ajout d'une colonne "arrival_date_month_number" qui converti le nom du mois en numéro de mois
    """)
    with st.expander("Voir le code python :"):
        st.code("""
map_month = {'January':"1", 'February':"2", 'March':"3", 'April':"4", 'May':"5", 'June':"6",
             'July':"7", 'August':"8", 'September':"9", 'October':"10", 'November':"11", 'December':"12"}

# Ajout d'une colonne calculé 'arrival_date_month_number' derivé de la colonne 'arrival_date_month'
df['arrival_date_month_number'] = df['arrival_date_month'].map(map_month)
        """)

    st.markdown("""
    - Calcul d'une colonne "arrival_date" de type date 
    """)
    with st.expander("Voir le code python :"):
        st.code("""
# Ajout d'une colonne de type date "arrival_date"
df['arrival_date'] = df['arrival_date_year'].astype('string') + '-' + df['arrival_date_month_number'] + '-' + df['arrival_date_day_of_month'].astype('string')
df['arrival_date'] = pd.to_datetime(df['arrival_date'])         
        """)

    st.markdown("""
    - Convertie au format datetime la colonne "reservation_status_date" 
    """)
    with st.expander("Voir le code python :"):
        st.code("""
        df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'])
        """)

    st.markdown("""
    - Calcul du nombre de nuité
    """)
    with st.expander("Voir le code python :"):
        st.code("""
df['Nb_total_nuit'] = df['reservation_status_date'] - df['arrival_date']
df['Nb_total_nuit'] = df['Nb_total_nuit'].dt.days
df['stays_total'] = df['stays_in_week_nights'] + df['stays_in_weekend_nights']    
    """)

    st.markdown("""
    - Ajout colonne departure_date = arrival_date + nb_stays pour les lignes not canceled
    """)
    with st.expander("Voir le code python :"):
        st.code("""
df['departure_date'] = df['arrival_date'] + pd.to_timedelta(df['stays_total'], unit='D')
df['departure_date'] = pd.to_datetime(df['departure_date'])
    """)

    st.markdown("""
    - Remplace les valeurs NA dans la colonne "children" par 0
    """)
    with st.expander("Voir le code python :"):
        st.code("""
    df["children"] = df['children'].fillna(0)
    """)

    st.markdown("""
    - Ajout du nombre total de client = nombre d'adultes + nombre d'enfants + nombre de bébés
    """)
    with st.expander("Voir le code python :"):
        st.code("""
    df['total_client'] = df['adults'] + df['children'] + df['babies']
    """)

    st.markdown("""
    - Créer un dataframe avec les reservations confirmées
    """)
    with st.expander("Voir le code python :"):
        st.code("""
    df_booked = df.loc[df['is_canceled']==0]
    """)

    st.markdown("""
    - Création d'une rangé de date depuis arrival_date jusqu'à departure_date
        Ceci afin de pouvoir calculer la durée moyenne de séjour concernant le client ou les clients.<br>
        Le résulat est stocké dans un dataframe afin de pouvoir le joindre au dataframe global pour effectuer des calculs de durée
    """,unsafe_allow_html=True)
    with st.expander("Voir le code python :"):
        st.code("""
df_booked = df_booked.loc[:,['arrival_date','departure_date','booking_id']]

def proc(row):
    dct = row.loc['booking_id':'booking_id'].to_dict()
    return pd.DataFrame({'Date': pd.date_range(row.arrival_date, row.departure_date)}).assign(**dct)

df_booked_date = pd.concat(df_booked.apply(proc, axis=1).tolist(), ignore_index=True)        
        """)

    st.markdown("""
    - Ajout de hiérarchies de date dans le dataframe "df_booked_date" : <br> - "Year" <br> - "Quarter" <br> - "Month Name" <br> - "Month Number" <br> - "Week Number" <br> - "Day of Month" <br> - "Day Name" <br> - "Day Number" <br> - "Day Type"
    """,unsafe_allow_html=True)
    with st.expander("Voir le code python :"):
        st.code("""
df_booked_date["Year"] = df_booked_date.Date.dt.year
df_booked_date["Quarter"] = df_booked_date.Date.dt.quarter
df_booked_date["Month Name"] = df_booked_date.Date.dt.month_name("fr")
df_booked_date["Month Number"] = df_booked_date.Date.dt.month
df_booked_date["Week Number"] = df_booked_date.Date.dt.week
df_booked_date["Day of Month"] = df_booked_date.Date.dt.day
df_booked_date["Day Name"] = df_booked_date.Date.dt.day_name("fr")
df_booked_date["Day Number"] = df_booked_date.Date.dt.day_of_week+1
df_booked_date["Day Type"] = df_booked_date.Date.dt.day_of_week.apply(lambda x: "Fin de semaine (weekend)" if x > 5 else "Jour de semaine")    
    """)

# Analyse 1 - 1 : analyse par mois et par années en graphique à bar
def load_analyse_1_1(a:Analyse,année:int):
    return a.analyse_1_1(année)
# Analyse 1 - 2 : analyse par semestre et par mois toutes années confondus en graphique boîte à moustache
def load_analyse_1_2(a:Analyse,semestre:int):
    return a.analyse_1_2(semestre)
# Analyse 1 - 3 : analyse par rapport au numéro du jour dans le mois ceci par années en graphique en camembert 
def load_analyse_1_3(a:Analyse,année:int):
    return a.analyse_1_3(année)

def load_view():
    col_a,col_b,col_c = st.columns([1,4,1])
    a = Analyse()
    a.read()

    with col_b:
        side_bar.load_sidebar()
        
        st.title("Analyse du dataset")
        load_problematique()

        select_slider_list_year = 2015,2016, 2017,"Toutes années"

        tab1, tab2 = st.tabs(["La transformation de données","L'analyse"])
        with tab1:
            st.subheader("La transformation de données")
            # with st.expander("Liste des transformations globales :"):
            load_transformation()

        with tab2:
            st.subheader("L'analyse :")
            with st.expander("Le meilleur moment pour être au calme avec le moins d'affluence possible"):
                choix_options = ["Par mois et par années - Graphique à Bar",
                                "Par semestre et par mois toutes années confondus - Graphique en Boîte à moustache",
                                "Par rapport au numéro du jour dans le mois par années - Graphique en Camember",
                                "Par rapport au jour de la semaine pour toutes les années - Grapqhique en Cluster"
                                ]
                choix_index = [1,2,3,4]
                choix_dict = dict(zip(choix_index,choix_options))

                choix = st.selectbox("Choisissez votre analyse :",options=choix_options,index=1)
                
                if choix == choix_dict[1]:
                    year = st.select_slider("Année ?", options=select_slider_list_year,label_visibility="visible")
                    if year == "Toutes années": year = 0
                    plt_graph = load_analyse_1_1(a, year)
                    st.pyplot(plt_graph)
                    st.markdown("""
                    
                    **Méthode de calcul de la fréquentation journaliére :**

        Pour ce calcul, on utilise le champ "Arrival Date" qui represente la date d'arrivée à l'hotel et le champ "Nb Stays" qui represente le nombre de nuitées.

        Ensuite, on calcule la date de départ suivant ces deux champs :<br>
                -"Date de départ" = "Date d'arrivée" + "Nombre de nuité"

        Enfin, pour chacune des dates présentes entre la date d'arrivée et la date de départ, on effectue une somme du nombre de client par jour puis la moyenne de cette même somme par mois :<br>
                - Somme(Nb Client) par jour => Moyenne(Somme(Nb Client) par jour) par mois
                    """,unsafe_allow_html=True)

                    st.markdown("""
                    **Analyse des graphiques** :
                    

        On a ici une representation par mois et par année de la moyenne jourrnalière de fréquentation sous forme de graphique à bar.

        Les 3 premiers graphiques representent respectivement l'année 2015 en bleu, l'année 2016 en orange et l'année 2017 en vert.<br>
        Pour chacun de ces 3 graphiques, le minimum est representé par une couleur rouge.<br>
        On remarque que pour les années 2015 et 2017, on ne possède pas d'année compléte. Ceci va donc fausser la moyenne globale par mois toutes années confondues (voir graphique "Toutes années").<br>

        Pour l'année 2015, on a un minimum de fréquentation journalière situé au mois de décembre.<br>
        Pour l'annèe 2016, ce même minimum se situe au mois de janvier.

        Enfin concernant l'année 2017, le minimum se situe au mois de Septembre. <br>
        Concernant ce dernier résultat, on constate que ce minimum est dû à un deficit de données. <br>
        En effet, le dataset couvre une période allant de Août 2015 à Août 2017 pour le champ "Arrival Date". (voir méthode de calcul de la fréquentation journalière)<br>

        On voit donc ici que l'on ne peut établir une tendance suivant le mois. <br>
        Cependant si l'on tient compte de 2016 qui est une année complète, on peut voir que le minimum se situe en Janvier.<br>
        Ceci est corroboré par le dernier graphique (noir) dont le minium est lui aussi situé au mois de Janvier.<br>

                    """,unsafe_allow_html=True)

                elif choix == choix_dict[2]:
                    st.markdown(choix_dict[2])

                    # Calcul des graphiques à moustache par semestre
                    plt_semestre1 = load_analyse_1_2(a,0)
                    plt_semestre2 = load_analyse_1_2(a,1)
                    
                    # Affichage des graphiques
                    st.pyplot(plt_semestre1)
                    st.pyplot(plt_semestre2)

                    # Affichage du texte de methode de calcul et d'analyse
                    st.markdown("""
                    **Methode de calcul :**<br>

Ici, on prend le total client brut par jour pour que le graphique puisse calculer la distribution journaliére selon le mois de l'année avec le min, le max, la mediane et le deux quantiles (25% et 75%). <br><br>
                    """,unsafe_allow_html=True)
                    st.markdown("""
                    **Analyse des graphiques :**<br>

On a ici deux graphiques boites à moustache, le premier represente le 1er semestre et le deuxième represente le 2eme semestre.<br>

Sur le graphique representant le premier semestre, on voit se dégager une tendance montante depuis le début du premier semestre vers la fin du premier semestre.<br>
Le minimum se situe ici en janvier. Ce qui vient confirmer l'analyse des graphique à bar.<br>
Pour janvier, on a un minimum à environ 300 et un maximum à presque 600.<br>
La médiane se situe un peu en dessous de 500.<br>

Sur celui representant le second semestre, on voite se dégager une tendance déscendante depuis le début du second semestre vers la fin du second semestre.<br>
On remarque un léger rebond en Octobre.<br>
Le minimum se situe lui au mois de Septembre, ceci est dû surement au déficit de données expliqué lors de l'analyse des graphiques à bar.<br>

On voit que **le minimum se situe bien en Janvier** ce qui vient corroboré nos analyses des grapiques à bar ci-dessus.<br><br>
                    """,unsafe_allow_html=True)


                elif choix == choix_dict[3]:
                    st.markdown(choix_dict[3])
                    year = st.select_slider("Année ?", options=select_slider_list_year,label_visibility="visible")
                    if year == "Toutes années": year = 0

                    # Calcul des graphiques
                    plt_graph = load_analyse_1_3(a, year)

                    # Affichage des graphiques
                    st.pyplot(plt_graph)

                    # Affichage Methode de calcul
                    st.markdown("""
                    **Méthode de calcul :**<br>

Ici, la fréquentation est calculé en 3 étapes :<br>
 **Etape 1 :** Somme(Nombre de client) par jour<br>
 **Etape 2 :** Création de catégorie "groupement de jours" selon le numéro du jour dans le mois :<br>
            -> "01 - 05" : inclus les jours 1, 2, 3, 4 et 5<br>
            -> "06 - 10" : inclus les jours 6, 7, 8, 9 et 10<br>
            -> "11 - 15" : inclus les jours 11, 12, 13, 14 et 15<br>
            -> "16 - 20" : inclus les jours 16, 17, 18, 19 et 20<br>
            -> "21 - 25" : inclus les jours 21, 22, 23, 24 et 25<br>
            -> "> 25"    : inclus tous les jours > 25<br>

 **Etape 3 :** Moyenne(Somme(Nombre de client) par jour) par "groupement de jours"<br>
                    """,unsafe_allow_html=True)

                    # Affichage Texte d'analyse
                    st.markdown("""
                    **Analyse des grapqhiques :**<br>

On a ici 4 graphiques camemberts.<br>
Les 3 premiers representent les années 2015, 2016 et 2017.<br>
Le dernier représente toutes les années.<br>
Sur chacun de ces graphiques, le minimum a été mis en evidence et a été détaché du reste du groupe.<br>

Sur l'année 2015, le minimum de fréquentation se situe sur les numéros de jour de 1 à 5.<br>
Sur les années 2016 et 2017, le minimum de fréquentation se situe sur les numéros de jour > 25.<br>
On voit ici que l'on arrive pas dégager une réelle tendance.<br>

Sur le dernier graphique representant toutes les années, le minimum se situe également sur les jours > 25.<br>
On remarque cependant que la différence n'est pas enorme par rapport aux autres groupement de jours.<br>

On peut en conclure que la fréquentation reste equilibré quel que soit le numéro de jour dans le mois.<br>
Si l'on avait pu avoir un jeu données plus conséquent, on aurait pu eventuellement y remarquer une tendance particulière.<br>
                    """,unsafe_allow_html=True)



                else:
                    st.markdown(choix_dict[4])

            with st.expander("Le meilleur moment pour avoir le plus de diversité en terme de pays représenté"):
                st.markdown("...")


            with st.expander("Le meilleur moment pour les voyages selon que l'on séjourne avec des enfants ou sans enfants"):
                st.markdown("...")


            with st.expander("Le meilleur moment pour bénéficier d'un sur-classement de type de chambre ou bien en terme de prix attractif "):
                st.markdown("...")

