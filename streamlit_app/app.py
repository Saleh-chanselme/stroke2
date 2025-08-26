import streamlit as st
import requests
import pandas as pd
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder
import matplotlib as plt
import plotly.express as px
import json



# Mettre toute l’application en pleine largeur
st.set_page_config(layout="wide") 


# App titre
st.title("Welcome to Stroke dataset")

# setting the tabs (nav bar)
home, data, visualization, statistics = st.tabs(["Home", "Data", "Visualization", "Statistics"])

# start home section 
with home:
    st.header("Stroke Data Analysis App")
    st.markdown("""Interactive web app that :red[visualizes] and :red[analyzes] patient data related to :red[stroke.]
Purpose: To explore stroke-related factors and present insights through clear visualizations.""")
# end home section 


# start data section(Début section Données ) ------------------------
with data:
    # section header (En-tête de la section)
    st.subheader("Patient Informations Form :")

    # Form 1: Search by ID( Formulaire 1 : Recherche par ID)
    with st.form("id_form"):
        st.caption("Search Patient By :red[Id]")
        patient_id = st.text_input("Patient ID")
        submit_id = st.form_submit_button("search")
        
        
    BASE_URL ="http://127.0.0.1:8000"
# Collect params only if forms are submitted(Récupérer les paramètres uniquement si le formulaire est soumis)
    params = {}
    url = f"{BASE_URL}/patients/{patient_id}"
    if 'submit_id' in locals() and submit_id:
        if patient_id:
            params["patient_id"] = patient_id
    try:
        # Only send request if params exist( Envoyer la requête uniquement si des paramètres existent)
        if params:  
            response = requests.get(url, params=params)
            data = response.json()

            # Convert JSON to DataFrame (Convertir le JSON en DataFrame)
            if isinstance(data, list):  
                df = pd.DataFrame(data)
            else:  
                # handle single patient (dict)/Cas d’un seul patient (dict)
                df = pd.DataFrame([data])

            # Show as interactive table in Streamlit(Afficher le tableau interactif dans Streamlit)
            st.dataframe(df, use_container_width=True)
            print(response.status_code)
            print(response.text)


        # else:
        #     st.info("Please enter filters or patient ID to search.")

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to API. Make sure the backend is running.")





#  Form 2: Patients filters (Formulaire 2 : Filtres patients )
    with st.form("my_form"):
        st.caption("Patients Filters")
        gender = st.selectbox("Gender", ["", "Male", "Female"])
        stroke = st.selectbox("Stroke", ["", "0", "1"])
        max_age = st.number_input("Max Age", min_value=0, max_value=120)
        submit_filter = st.form_submit_button("Search")

    # ---- Fetch and display data if form submitted (Récupérer et afficher les données si le formulaire est soumis)----
    if submit_filter:
        params = {}
        if gender:
            params["gender"] = gender
        if stroke:
            params["stroke"] = stroke
        if max_age:
            params["max_age"] = max_age
            
        BASE_URL = "http://127.0.0.1:8000"
        url = f"{BASE_URL}/patients/"

        try:
            # Only send request if params exist(Envoyer la requête uniquement si des paramètres existent)
            if params:  
                response = requests.get(url, params=params)
                data = response.json()

                # Convert JSON to DataFrame(Convertir le JSON en DataFrame)
                if isinstance(data, list):
                    df = pd.DataFrame(data)
                else:
                    df = pd.DataFrame([data])

                if not df.empty:
                    # Configure AgGrid for full width(Configurer AgGrid pour pleine largeur)
                    gb = GridOptionsBuilder.from_dataframe(df)
                    gb.configure_default_column(resizable=True, sortable=True, filter=True)
                    gb.configure_grid_options(domLayout='autoHeight')  # auto height(hauteur automatique)
                    gridOptions = gb.build()

                    st.subheader("Patients Data")
                    AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=False, fit_columns_on_grid_load=True, height=700)
                else:
                    st.info("No data found for these filters.")

        except requests.exceptions.ConnectionError:
            st.error("Could not connect to API. Make sure the backend is running.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
# end data section(Fin section Données) -------------------------


# start visual section(Début section Visualisation) ------------------
with visualization:
    st.subheader("Stroke Data Visual Analytics")


    try:
        # Request data from API(Récupérer les données depuis l’API)
        response = requests.get("http://127.0.0.1:8000/patients/")
        
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data if isinstance(data, list) else [data])
            
            if not df.empty and 'stroke' in df.columns:
                # Chart 1: Stroke Distribution(Graphique 1 : Répartition des AVC)
                counts = df['stroke'].value_counts()
                counts.index = counts.index.map({0: 'Without Stroke', 1: 'With Stroke'})
                fig1 = px.pie(names=counts.index, values=counts.values, title="Stroke Distribution")
                st.plotly_chart(fig1)
                
                # Chart 2: Average BMI per Stroke Status(Graphique 2 : BMI moyen par statut AVC)
                if 'bmi' in df.columns:
                    avg_bmi = df.groupby('stroke')['bmi'].mean().reset_index()
                    avg_bmi['stroke'] = avg_bmi['stroke'].map({0: 'Without Stroke', 1: 'With Stroke'})
                    
                    fig2 = px.bar(
                        avg_bmi,
                        x='stroke',
                        y='bmi',
                        title="Average BMI by Stroke Status",
                        labels={'stroke': 'Stroke Status', 'bmi': 'Average BMI'},
                        text='bmi',
                        color='stroke'
                    )
                    st.plotly_chart(fig2)
                    
                # Chart 3:Pie chart Fumeurs vs Non-fumeurs ----------------
                st.markdown("### Smokers vs Non-Smokers among Stroke Patients")
                # Filtrer uniquement les patients ayant eu un AVC
                stroke_df = df[df['stroke'] == 1]
                # Compter fumeurs vs non-fumeurs
                stroke_smoking_counts = stroke_df['smoking_status'].apply(
                    lambda x: 'Fumeur' if x != 'never smoked' else 'Non-fumeur'
                ).value_counts()
                # Créer le pie chart avec Plotly
                fig_smoking = px.pie(
                    names=stroke_smoking_counts.index,
                    values=stroke_smoking_counts.values,
                    title="Stroke Patients: Smokers vs Non-Smokers"
                )
                st.plotly_chart(fig_smoking, use_container_width=True, key="pie_smoking")

            else:
                st.warning("No valid stroke data found in the dataset.")
        else:
            st.error("Failed to fetch data from API")

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to API")
    except Exception as e:
        st.error(f"Erreur lors du chargement des visualisations : {e}")


# end visual section(Fin section Visualisation) -------------------------------------------
        
# start statistic section(Début section Statistiques) --------------------------------------        
with statistics:
    st.subheader("Pateints Descriptive Statistics")
        
        
    BASE_URL ="http://127.0.0.1:8000"
    params = {}
    url = f"{BASE_URL}/stats/"
    try:
            response = requests.get(url, params=params)
            data = response.json()

            # Convert JSON to DataFrame(Convertir le JSON en DataFrame)
            if isinstance(data, list):  
                df = pd.DataFrame(data)
            else:  
                # handle single patient (dict)/Cas d’un seul patient (dict)
                df = pd.DataFrame([data])

            # Show as interactive table in Streamlit(Afficher le tableau interactif dans Streamlit)
            st.dataframe(df, use_container_width=True)
            print(response.status_code)
            print(response.text)
            

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to API. Make sure the backend is running.")
# end statistic section (Fin section Statistiques)--------------------------------------        
