import streamlit as st
from src.views.components import side_bar
from src.controllers.analyse import Analyse

def load_problematique():
    st.subheader("La problèmatique :")

    st.markdown("""
    Ce jeu de données a été analysé selon la problématique suivante :

    Quel est le meilleur moment pour réserver une chambre d'hôtel selon ces 4 angles de vue : 
    1) Le meilleur moment pour être au calme avec le moins d'affluence possible
    2) Le meilleur moment pour avoir le plus de diversité en termes de pays représentés
    3) Le meilleur moment pour les voyages selon que l'on séjourne avec des enfants ou sans enfants
    4) Le meilleur moment pour bénéficier d'un sur-classement de type de chambre 
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
# Analyse 1 - 4 : analyse par rapport au type de jour (Week end / Jour de semaine) toutes années confondus en graphique cluster
def load_analyse_1_4(a:Analyse,graph_type:str):
    return a.analyse_1_4(graph_type)
# Analyse 2 - 1 : distribution de la diversité des pays par mois et par années
def load_analyse_2_1(a:Analyse,année:int):
    return a.analyse_2_1(année)
# Analyse 2 - 2 : top 3 des pays les plus representé selon le mois et l'année
def load_analyse_2_2(a:Analyse, année:int):
    return a.analyse_2_2(année)
# Analyse 3 - 1 : distribution par catégorie (Enfants / Sans enfants) selon le mois et l'année
def load_analyse_3_1(a:Analyse, année:int):
    return a.analyse_3_1(année)
# Analyse 3 - 2 : graphique polaire par sous catégorie (Couple, Seule, Groupe, Enfants seules) par mois toutes années confondues
def load_analyse_3_2(a:Analyse):
    return a.analyse_3_2()
# Analyse 4 - 1 : HeatMap répartition des surclassements, déclassements et inchangées
def load_analyse_4_1(a:Analyse):
    return a.analyse_4_1()
# Analyse 4 - 2 : Linechart de répartition des surclassements, déclassements et inchangées selon le mois toutes années confondues
def load_analyse_4_2(a:Analyse):
    return a.analyse_4_2()


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
            with st.expander("📅 - **1) Le meilleur moment pour être au calme avec le moins d'affluence possible**"):
                choix_options = ["Par mois et par années - Graphique à Bar",
                                "Par semestre et par mois toutes années confondus - Boîte à moustache",
                                "Par rapport au numéro du jour dans le mois par années - Camembert",
                                "Par rapport au jour de la semaine pour toutes les années - Cluster"
                                ]
                choix_index = [1,2,3,4]
                choix_dict = dict(zip(choix_index,choix_options))

                st.markdown("""
                #### Le but de cette analyse est de pouvoir dégager une tendance temporelle via différent angle de vue : <br>
a) Fréquentation par rapport au mois et à l'année <br>
b) Distribution par rapport au semestre et au mois <br>
c) Fréquentation par rapport au numéro du jour dans le mois <br>
d) Fréquentaton par rapport au jour de la semaine
                """,unsafe_allow_html=True)

                choix = st.selectbox("Choisissez votre analyse :",options=choix_options,index=1)
                
                if choix == choix_dict[1]:

                    year = st.select_slider("Année ?", options=select_slider_list_year,label_visibility="visible",key="slider_analyse_1_1")

                    if year == "Toutes années": year = 0

                    plt_graph = load_analyse_1_1(a, year)

                    st.pyplot(plt_graph)
                    st.markdown("""
                    #### **<u>Méthode de calcul de la fréquentation journaliére :</u>**

        Pour ce calcul, on utilise le champ "Arrival Date" qui represente la date d'arrivée à l'hotel et le champ "Nb Stays" qui represente le nombre de nuitées.

        Ensuite, on calcule la date de départ suivant ces deux champs :<br>
                -"Date de départ" = "Date d'arrivée" + "Nombre de nuité"

        Enfin, pour chacune des dates présentes entre la date d'arrivée et la date de départ, on effectue une somme du nombre de client par jour puis la moyenne de cette même somme par mois :<br>
                - Somme(Nb Client) par jour => Moyenne(Somme(Nb Client) par jour) par mois
                    """,unsafe_allow_html=True)

                    st.markdown("""
                    #### **<u>Analyse des graphiques :</u>**                    

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
                    # st.markdown(choix_dict[2])

                    # Calcul des graphiques à moustache par semestre
                    plt_semestre1 = load_analyse_1_2(a,0)
                    plt_semestre2 = load_analyse_1_2(a,1)
                    
                    # Affichage des graphiques
                    st.pyplot(plt_semestre1)
                    st.pyplot(plt_semestre2)

                    # Affichage du texte de methode de calcul et d'analyse
                    st.markdown("""
                    #### **<u>Methode de calcul :</u>**<br>

Ici, on prend le total client brut par jour pour que le graphique puisse calculer la distribution journaliére selon le mois de l'année avec le min, le max, la mediane et le deux quantiles (25% et 75%). <br><br>
                    """,unsafe_allow_html=True)
                    st.markdown("""
                    #### **<u>Analyse des graphiques :</u>**<br>

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
                    # st.markdown(choix_dict[3])
                    year = st.select_slider("Année ?", options=select_slider_list_year,label_visibility="visible",key="slider_analyse_1_3")
                    if year == "Toutes années": year = 0

                    # Calcul des graphiques
                    plt_graph = load_analyse_1_3(a, year)

                    # Affichage des graphiques
                    st.pyplot(plt_graph)

                    # Affichage Methode de calcul
                    st.markdown("""
                    #### **<u>Méthode de calcul :</u>**<br>

Ici, la fréquentation est calculé en 3 étapes :<br>

 **<u>Etape 1 :</u>** Somme(Nombre de client) par jour<br>

 **<u>Etape 2 :</u>** Création de catégorie "groupement de jours" selon le numéro du jour dans le mois :<br>
            -> "01 - 05" : inclus les jours 1, 2, 3, 4 et 5<br>
            -> "06 - 10" : inclus les jours 6, 7, 8, 9 et 10<br>
            -> "11 - 15" : inclus les jours 11, 12, 13, 14 et 15<br>
            -> "16 - 20" : inclus les jours 16, 17, 18, 19 et 20<br>
            -> "21 - 25" : inclus les jours 21, 22, 23, 24 et 25<br>
            -> "> 25"    : inclus tous les jours > 25<br>

 **<u>Etape 3 :</u>** Moyenne(Somme(Nombre de client) par jour) par "groupement de jours"<br>
                    """,unsafe_allow_html=True)

                    # Affichage Texte d'analyse
                    st.markdown("""
                    #### **<u>Analyse des grapqhiques :</u>**<br>

On a ici 4 graphiques camembert.<br>
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
                    choix_options = ["Par type de jour - Weekend / Jour de la semaine",
                                    "Par jour de la semaine : Lundi, Mardi..."
                                    ]
                    choix_index = ["CLUSTER","PIE"]
                    choix_dict = dict(zip(choix_options,choix_index))

                    choix = st.selectbox("Choisissez le périmètre de l'analyse :",options=choix_options,index=1)

                    # Calcul du graphique 
                    plt_graph = load_analyse_1_4(a, choix_dict[choix])

                    # Affichage du graphique
                    st.pyplot(plt_graph)

                    # Affichage Méthode de calcul
                    st.markdown("""
                        #### **<u>Méthode de calcul :</u>** <br>

Ici, la moyenne de fréquentation a été calculé en deux étapes :<br>

**<u>Etape 1 :</u>** Somme(Nombre de client) par semaines et par années<br>

**<u>Etape 2 :</u>** Moyenne(Somme(Nombre de client) par semaines et par années) par jour de la semaine<br>
                        """,unsafe_allow_html=True)

                    if choix_dict[choix] == "CLUSTER":

                        # Affichage Texte analyse
                        st.markdown("""
                        #### **<u>Analyse du graphique cluster :</u>**<br>

Ici, on a une representation sous forme de cluster.<br>
La répartition est sur le type de jour "Jour de la semaine" ou bien "Fin de semaine".<br>
On voit ici que la réparation est equilibré en 50/50.<br>

                        """,unsafe_allow_html=True)
                    else:
                        # Affichage Texte analyse
                        st.markdown("""
                        #### **<u>Analyse du graphique camember :</u>**<br>

Ici, on a une répartition de la fréquentation par rapport au jour de la semaine.<br>
Le minimum a été mis en evidence et a été séparé des autres jours de la semaine.<br>
Le minimum se situe à Mardi avec une valeur de 13%.<br>

La différence par rapport aux autres jours de la semaine est minime.

                        """,unsafe_allow_html=True)               

            st.markdown("""
            ### Conclusion des analyses de fréquentation par rapport à la période :<br>

On a pu voir d'après les analyses précedentes et les differents point de vue temporel une tendance se degager sur la moyenne de fréquentation journalière.<br>

Le meilleur mois pour une faible fréquentation se situe en Janvier.<br>

Pour le jour dans le mois, ce sont les jours supérieur à 25 qui enregistrent le moins de fréquentation. <br>
Cependant la différence reste faible par rapport aux  autres jours dans le mois.<br>

En ce qui concerne le jour de la semaine, c'est le Mardi qui est le plus faible en fréquentation.<br>
La répartition "Jour de la semaine" / "Fin de semaine" est plutôt equilibré 50/50.

            """,unsafe_allow_html=True)

            with st.expander("🌍 - **2) Le meilleur moment pour avoir le plus de diversité en terme de pays représenté**"):
                st.markdown("""
                ### Le but de cette analyse est de pouvoir :<br>
a) Identifier le mois de l'année dans lequel on a le plus de diversité de pays<br>
b) Identifier le top 3 des pays les plus representés selon le mois de l'année<br>

Par diversité, on entend le moment où l'on a le plus de pays différents representés dans le mois.<br>
                """,unsafe_allow_html=True)

                choix_options = ["Diversité des pays par mois et par années",
                                "TOP 3 des pays les plus representés selon le mois de l'année"
                                    ]
                choix_index = ["DISTRIBUTION","TOP"]
                choix_dict = dict(zip(choix_options,choix_index))

                choix = st.selectbox("Choisissez le perimètre d'analyse",options=choix_options)

                year = st.select_slider("Année ?", options=select_slider_list_year,label_visibility="visible",key="slider_analyse_2")
                if year == "Toutes années": year = 0

                if choix_dict[choix] == "DISTRIBUTION":
                    # Calcul du graphique
                    plt_graph = load_analyse_2_1(a,year)

                    # Affichage du graphique
                    st.pyplot(plt_graph)

                    # Affichage Methode de calcul
                    st.markdown("""
                    #### **<u>Méthode de calcul :</u>**<br>

Le nombre de pays unique est calculé selon cette methode :<br>

    Nb Pays Unique = Count Distinct(Pays) pas années et par mois<br>
                    """,unsafe_allow_html=True)

                    # Affichage Texte analyse
                    st.markdown("""
                    #### **<u>Analyse des graphiques :</u>**<br>

Les 3 premiers graphiques ci-dessus representent le nombre de pays unique par mois et pas années.<br>
Sur chacun de ces 3 graphiques le maximum a été mis en evidence en rouge.<br>

Pour l'année 2015, on a un maximum sur le mois d'Octobre.<br>
Pour l'année 2016, le maximum se situe en Novembre.<br>
Enfin pour l'année 2017, le maximum se situe en Avril.<br>

Le dernier grapqhique (en noir) represente le nombre de pays unique representé par mois pour toutes les années.<br>
Le maximum se situe en Juin. Les mois d'Avril, Mai, Octobre et Novembre se rapproche du maximum.<br>

                    """,unsafe_allow_html=True)

                else:
                    # Calcul du graphique
                    plt_graph = load_analyse_2_2(a,year)
                    
                    # Affichage du graphique
                    st.pyplot(plt_graph)

                    # Affichage Methode de calcul
                    st.markdown("""
                    #### **<u>Méthode de calcul :</u>**<br>

Le calcul de la moyenne de fréquentation par pays est effectué en 2 etapes :<br>

**<u>Etape 1 :**</u> Somme(Nombre de client) par années, par pays, par mois et par jour<br>

**<u>Etape 2 :**</u> Moyenne(Résultat Etape 1) par année, pays et mois<br>
                    """,unsafe_allow_html=True)

                    # Affichage Texte analyse
                    st.markdown("""
                    #### **<u>Analyse des graphiques :</u>**<br>
Les graphiques ci-dessus representent la moyenne de fréquentation journaliéré par rapport au pays d'origine du client.<br>
Les 3 premieres graphiques representent les années 2015, 2016 et 2017 découpés par mois.<br>

Sur l'année 2015, les 4 pays les plus representatifs sont la France (FRA), l'Espagne (ESP), le Portugal (PRT) et l'Angleterre (GBR).<br>
On remarque ici un net domination du Portugal sur tous les mois.<br>

Pour l'année 2016, les 5 pays les plus representatifs sont la France (FRA), l'Espagne (ESP), le Portugal (PRT), l'Angleterre (GBR) et l'Allemagne (DEU).<br>
On remarque ici une nette domination du Portugal suivi de l'Angleterre et enfin de la France.<br>

Enfin pour l'année 2017, les 5 pays les plus representatifs la France (FRA), le Portugal (PRT), l'Angleterre (GBR), l'Allemagne (DEU) et la Suède (SWE).<br>
Comme sur l'année 2016, on a une nette domination du Portugal suivi de l'Angleterre et enfin de la France. <br>

Sur le graphique final, on a une moyenne toutes années confondues de la fréquentation journalière par pays.<br>
On voit encore ici une forte domination du Portugal, suivi de l'Angleterre et de la France.<br>
                    """,unsafe_allow_html=True)


            st.markdown("""
            ### **Conclusions des analyses sur la fréquentation par pays :**<br>

Sur les graphiques du nombre de pays unique, on a pu voir que les mois de l'année representant le plus de diversité en terme de pays sont Avril, Mai, Juin et également sur Octobre et Novembre.<br>

Sur les graphiques representant les pays les plus présents en terme de fréquence, on s'appercoit que 3 pays reviennent le plus souvent : France, Portugal et Angleterre.<br>
                """,unsafe_allow_html=True)

            with st.expander("👨‍👩‍👧‍👦 - **3) Le meilleur moment pour les voyages selon que l'on séjourne avec des enfants ou sans enfants**"):
                st.markdown("""
### **Le but de cette analyse est de pouvoir détécter les tendances catégories de clients et de sous-catégories de clients :**<br>
Les **catégories** clients sont :
- Client avec enfants<br>
- Client sans enfants<br>

<br>Les **sous-catégories** de client suivantes :
- Couple<br>
- Personne seule<br>
- Groupe <br>
- Enfants non accompagnés (uniquement pour la cétégorie "Avec Enfants")<br>

<br>Ceci permettra de pouvoir choisir la période la plus propice pour :
 - les voyages avec enfants pour pouvoir profiter d'une atmoshpère plus familiale <br>
 - ou bien ceux préférant le moment où il y a le moins d'enfants pour plus de tranquilité par exemple<br>
 <br>
                """,unsafe_allow_html=True)

                choix_options = ["Par catégorie client - Graphique à bar",
                                "Par sous catégorie de client - Graphique polaire"
                                    ]
                choix_index = ["CATEGORIE","SOUS-CATEGORIE"]
                choix_dict = dict(zip(choix_options,choix_index))

                choix = st.selectbox("**Choisissez le perimètre d'analyse**",options=choix_options)

                if choix_dict[choix] == "CATEGORIE":
                    year = st.select_slider("Année ?", options=select_slider_list_year,label_visibility="visible",key="slider_analyse_3_1")
                    if year == "Toutes années": year = 0

                    # Calcul du graphique
                    plt_graph = load_analyse_3_1(a,year)
                        
                    # Affichage du graphique
                    st.pyplot(plt_graph)

                    # Affichage Methode de calcul
                    st.markdown("""
#### **<u>Méthode de calcul :**</u><br>

Le calcul des fréquentations par catégories est effectué en deux etapes :<br>

 **<u>Etape 1</u>** : Count(Catégorie) par année, mois et jours<br>
 
 **<u>Etape 2</u>** : Moyenne(Résultat Etape 1) par année et mois<br>
                    """,unsafe_allow_html=True)

                    # Affichage Texte analyse
                    st.markdown("""
#### **<u>Analyse des graphiques :**</u><br>

Les graphiques ci-dessus représente pour les années 2015, 2016 et 2017 une moyenne en % des réservations par mois et catégorie client.<br>

Pour l'année 2015, on a pour la catégorie "Sans Enfants" un maximum sur le mois de Septembre et un minimum sur le mois Juillet.<br>
Pour la catégorie "Avec Enfants", on a un maximum en Août et un minimum en Novembre.<br>

Pour l'année 2016, on a pour la catégorie "Sans Enfants" un maximum sur le mois de Septembre et un minimum sur le mois de Janvier.<br>
Pour la catégorie "Avec Enfants", on a un maximum au mois d'Août et un minimum en Janvier.<br>

Pour l'année 2017, on a pour la catégorie "Sans Enfants" pour le mois de Mai et un minimum sur le mois de Septembre.<br>
Pour la catégorie "Avec Enfants", on a un maximum au mois d'Août et un minimum sur le mois de Septembre. <br>
Ceci est dû au deficit décrit lors des précedentes analyses.<br>

D'un point de vue global, le dernier graphique permet de voir la répartition toutes années confondues.<br>
Pour la catégorie "Sans Enfants", on a un maximum en Mai et un minimum en Janvier/Décembre.<br>
Pour la catégorie "Avec Enfants", on a un maximum en Août et un minimum en Novembre.<br>
                    """,unsafe_allow_html=True)

                else:
                    # Affichage Texte introduction
                    st.markdown("""
                    #### **<u>Graphique par Sous Catégorie :</u>**
- Couple (Toutes catégories)
- Groupe (Toutes catégories)
- Personne Seule (Toutes catégories)
- Enfants non accompagnés (Catégorie 'Avec Enfants')
                    """,unsafe_allow_html=True)

                    # Calcul du graphique
                    plt_graph_list = load_analyse_3_2(a)
                        
                    # Affichage du graphique
                    for plt_graph in plt_graph_list:
                        st.pyplot(plt_graph)

                    # Affichage Methode de calcul
                    st.markdown("""
#### **<u>Méthode de calcul :</u>**<br>

Le calcul des fréquentations par sous-catégories est effectué en 2 étapes :<br>

**<u>Etape 1 :</u>** Count(Réservation) par Année, Catégorie, Sous catégorie, Mois, Jour<br>

**<u>Etape 2 :</u>** Moyenne(Résultat Etape 1) par Année, Catégorie, Sous catégorie, Mois<br>
                    """,unsafe_allow_html=True)

                    # Affichage Texte analyse
                    st.markdown("""
                    #### **<u>Analyse des graphiques :</u>**<br>
On ici 2 graphiques représentant chacun une décomposition des catégories "Avec Enfants" et "Sans Enfants".<br>
La décomposition s'effectue par mois en fonction du pourcentage du nombre de réservation.<br>

Sur le premier graphique "Avec Enfants", on peut voir que la catégorie couples avec enfants est dominante.<br>
Elle est majoritaire sur le mois d'Août.
La catégorie "Enfants non accompagnés" est majoritaire sur le mois Novembre.<br>
La catégorie personne seule avec enfants est majoritairement présente sur les mois de Janvier, Février et Octobre.<br>
En ce qui concerne la catégorie groupe avec enfants, elle est plutôt minime et est majoritaire sur le mois de Janvier.<br>

Sur le second graphique "Sans Enfants", on a toujours une nette domination de la sous-catégorie "Couple".<br>
La catégorie "Personne seule" se situe en deuxiéme position en terme de volume de réservation. <br>
On a un maximum en Janvier et un minimum en Juillet/Août.<br>
Pour la catégorie "Groupe", on a un maximum en Juillet/Août et un minimum en Novembre.
                    """,unsafe_allow_html=True)

            # Affichage Conclusions Analyse 3
            st.markdown("""
                ### **Conclusions des analyses par "Catégorie Client" et "Sous-catégorie Client" :**<br>

D'après le graphique de répartition par mois et année, on en conclus ceci :<br>
Pour les personnes souhaitant le calme sans enfants, il est préferable de réserver en Mai ou en Novembre.<br>
D'un autre côté ceux souhaitant jouir d'une atmosphére plus familiale doivent réserver en Août.<br>

Si l'on s'interesse au type de client à savoir Couple, Groupe ou Personne seules, on en conclus ceci :<br>
Les personnes seules sont plus nombreuses à reserver au mois de Janvier et Novembre.<br>
Les couples quant à eux sont plus nombreux à réserver en Juillet/Août.<br>
Les groupes sont également plus nombreux au mois Juillet/Août.<br>

Enfin en ce qui concerne les enfants non accompagnés, ils sont plus nombreux au mois de Novembre.<br>

                """,unsafe_allow_html=True)

            with st.expander("💳 - **4) Le meilleur moment pour bénéficier d'un sur-classement de type de chambre ou bien en terme de prix attractif**"):
                # Affichage Introduction
                st.markdown("""
                #### **Le but de cette analyse est :**<br>
a) Visualiser la répartition des surclassements et des déclassement de chambre d'hotel :<br>
> Rappel : les types de chambres sont catégorisés par lettre allant de A à L<br>
b) Visualiser cette même répartition selon les mois de l'année<br>

                """,unsafe_allow_html=True)

                # Choix Périmètre analyse
                choix_options = ["a) Surclassement et Déclassement par répartition - Heatmap",
                "b) Surclassement et Déclassement par mois - Histogramme"
                    ]
                choix_index = ["HEATMAP","HISTO"]
                choix_dict = dict(zip(choix_options,choix_index))

                choix = st.selectbox("**Choisissez le perimètre d'analyse**",options=choix_options)

                if choix_dict[choix] == "HEATMAP":
                    
                    # Calcul du graphique
                    plt_graph = load_analyse_4_1(a)

                    # Affichage du graphique
                    st.pyplot(plt_graph)

                    # Affichage Méthode de calcul
                    st.markdown("""
                    #### **<u>Méthode de calcul :</u>**<br>
Pour effectuer une visualisation graphique sous forme de heat map, on a ici besoin de calculer 3 matrices.<br>
Une matrice pour les surclassements, un deuxième pour les déclassements et une troisième pour les inchangées.<br>

<u>Calcul de la matrice SURCLASSEMENT :</u> <br>
> Etape 1 : Somme(Surclassement)<br>
> Etape 2 : Tableau croisée en ligne les chambres reservées, en colonne les chambres assignées, en indicateur la somme des surclassements<br>
> Etape 3 : On divise l'indicateur du tableau croisé par la somme des surclassements de l'Etape 1<br>
> Etape 4 : on remplace les valeurs à 0 par des NA (pour eviter d'interferer avec les valeurs de declassement et inchangées)<br>

<u>Calcul de la matrice DECLASSEMENT :</u><br>
> On applique la même méthode que les SURCLASSEMENT en remplaçant l'indicateur par la somme des déclassements<br>

<u>Calcul de la matrice INCHANGEE :</u><br>
> On applique la même méthode que les SURCLASSEMENT en remplaçant l'indicateur par la somme des inchangées<br>
                    """,unsafe_allow_html=True)

                    # Affichage Texte Analyse
                    st.markdown("""
                    #### **<u>Analyse du graphique :</u>**<br>
D'après les analyses du graphique, on en conclus que :<br>

<u>Pour les SURCLASSEMENTS :</u><br>
>* Les forts taux de suclassement se situent sur les catégories B vers A (19%) et D vers A (49%)<br>
>* Les plus faibles taux de surclassement se situent sur les  catégories C et L<br>

<u>Pour les DECLASSEMENTS :</u><br>
>* Les plus forts de taux de déclassement se situent sur les catégories A vers D (52%), A vers E (7.8%) et D vers E (5.7%)<br>

<u>Pour les INCHANGEES :</u><br>
>* Pour les inchangées, les plus fort taux se situent sur les catégories A (62%) et D(22%)<br>
>* Les plus faibles sont situés sur les catégories B (<1%), C(1.14%), H(<1%)<br>
                    """,unsafe_allow_html=True)

                else:
                    # Calcul du graphique
                    plt_graph = load_analyse_4_2(a)

                    # Affichage du graphique
                    st.pyplot(plt_graph)

                    # Affichage Méthode de calcul
                    st.markdown("""
                    #### **<u>Méthode de calcul :</u>**<br>
Pour effectuer une visualisation graphique sous forme d'histogramme, on a besoin des 3 indicateurs suivants : <br>
* Total Surclassement par mois<br>
* Total Déclassement par mois<br>
* Total des Inchangés par mois<br>""",unsafe_allow_html=True)
                    st.markdown(""" """)
                    st.markdown("""
Ensuite, on calcule le ratio par mois par rapport au total sur l'année, on multiplie le tout par 100 pour obtenir le pourcentage :<br>
* Ratio Déclassement = Total des déclassementss par mois / Total des déclassements sur l'année * 100<br> 
* Ratio Surclassement = Total des surclassements par mois / Total des surclassements sur l'année * 100<br>
* Ratio Inchangée = Total des inchangées par mois / Total des inchangées sur l'année * 100<br>
                    """,unsafe_allow_html=True)

                    # Affichage Texte Analyse
                    st.markdown("""
                    #### **<u>Analyse du graphique :</u>**<br>
D'après les analyses du graphique, on en conclus que :<br>

<u>Pour les SURCLASSEMENTS (Courbe en bleu) :</u><br>
> * On a 2 pics, le premier en Mars et le deuxième en Juillet<br>
> * On a 2 fortes baisses en Mai et en Novembre<br>

<u>Pour les DECLASSEMENTS (Bar en rouge) :</u><br>
> * On a 2 gros pics en Septembre et en Octobre<br>
> * Les moments les plus faibles sont en Juin et Juillet<br>

<u>Pour les INCHANGEES (Courbe en vert) :</u><br>
>* On un gros pic en Août<br>
>* Les moments les plus faibles se situent en début et fin d'année<br>
                    """,unsafe_allow_html=True)


            st.markdown("""
                ### **Conclusions des analyses des "surclassements" et "déclassements" de chambre d'hôtel :**<br>
Concernant le meilleur type de chambre à choisir pour bénéficier d'un surclassement, on a dans l'ordre décroissant :<br>
>* Les chambres de type D (49% de surclassement)<br>
>* Les chambres de type B (19% de surclassement)<br>
>* Les chambres de type F (~8% de surclassement)<br>

Concernant les meilleurs moments de l'année pour bénéficier d'un surclassement, on a :<br>
>* La période allant de Juillet à Août<br>
Il faut éviter les débuts et fins d'année et les mois de Septembre et Octobre qui enregistre les plus forts taux de déclassement de chambre.<br>
                """,unsafe_allow_html=True)



