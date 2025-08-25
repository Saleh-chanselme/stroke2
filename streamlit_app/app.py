import streamlit as st
import requests
import pandas as pd
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder
import matplotlib as plt
import plotly.express as px
import json



# Make the entire app full width
st.set_page_config(layout="wide") 


# App title 
st.title("Welcome to Stroke dataset")

# setting the tabs (nav bar)
home, data, visualization, statistics = st.tabs(["Home", "Data", "Visualization", "Statistics"])

# start home section 
with home:
    st.header("Stroke Data Analysis App")
    st.markdown("""Interactive web app that :red[visualizes] and :red[analyzes] patient data related to :red[stroke.]
Purpose: To explore stroke-related factors and present insights through clear visualizations.""")
# end home section 


# start data section ------------------------
with data:
    # section header 
    st.subheader("Patient Informations Form :")

    # Form 1: Search by ID
    with st.form("id_form"):
        st.caption("Search Patient By :red[Id]")
        patient_id = st.text_input("Patient ID")
        submit_id = st.form_submit_button("search")
        
        
    BASE_URL ="http://127.0.0.1:8000"
# Collect params only if forms are submitted
    params = {}
    url = f"{BASE_URL}/patients/{patient_id}"
    if 'submit_id' in locals() and submit_id:
        if patient_id:
            params["patient_id"] = patient_id
    try:
        # Only send request if params exist
        if params:  
            response = requests.get(url, params=params)
            data = response.json()

            # Convert JSON to DataFrame
            if isinstance(data, list):  
                df = pd.DataFrame(data)
            else:  
                # handle single patient (dict)
                df = pd.DataFrame([data])

            # Show as interactive table in Streamlit
            st.dataframe(df, use_container_width=True)
            print(response.status_code)
            print(response.text)


        # else:
        #     st.info("Please enter filters or patient ID to search.")

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to API. Make sure the backend is running.")





#  Form 2: Patients filters 
    with st.form("my_form"):
        st.caption("Patients Filters")
        gender = st.selectbox("Gender", ["", "Male", "Female"])
        stroke = st.selectbox("Stroke", ["", "0", "1"])
        max_age = st.number_input("Max Age", min_value=0, max_value=120)
        submit_filter = st.form_submit_button("Search")

    # ---- Fetch and display data if form submitted ----
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
            # Only send request if params exist
            if params:  
                response = requests.get(url, params=params)
                data = response.json()

                # Convert JSON to DataFrame
                if isinstance(data, list):
                    df = pd.DataFrame(data)
                else:
                    df = pd.DataFrame([data])

                if not df.empty:
                    # Configure AgGrid for full width
                    gb = GridOptionsBuilder.from_dataframe(df)
                    gb.configure_default_column(resizable=True, sortable=True, filter=True)
                    gb.configure_grid_options(domLayout='autoHeight')  # auto height
                    gridOptions = gb.build()

                    st.subheader("Patients Data")
                    AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=False, fit_columns_on_grid_load=True, height=700)
                else:
                    st.info("No data found for these filters.")

        except requests.exceptions.ConnectionError:
            st.error("Could not connect to API. Make sure the backend is running.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
# end data section -------------------------


# start visual section ------------------
with visualization:
    st.subheader("Stroke Data Visual Analytics")


    try:
        # Request data from API
        response = requests.get("http://127.0.0.1:8000/patients/")
        
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data if isinstance(data, list) else [data])
            
            if not df.empty and 'stroke' in df.columns:
                # Chart 1: Stroke Distribution
                counts = df['stroke'].value_counts()
                counts.index = counts.index.map({0: 'Without Stroke', 1: 'With Stroke'})
                fig1 = px.pie(names=counts.index, values=counts.values, title="Stroke Distribution")
                st.plotly_chart(fig1)
                
                # Chart 2: Average BMI per Stroke Status
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
            else:
                st.warning("No valid stroke data found in the dataset.")
        else:
            st.error("Failed to fetch data from API")

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to API")
    except Exception as e:
        st.error(f"Error: {e}")



# end visual section -------------------------------------------
  
  
  
        
# start statistic section --------------------------------------        
with statistics:
    st.subheader("Pateints Descriptive Statistics")
        
        
    BASE_URL ="http://127.0.0.1:8000"
    params = {}
    url = f"{BASE_URL}/stats/"
    try:
            response = requests.get(url, params=params)
            data = response.json()

            # Convert JSON to DataFrame
            if isinstance(data, list):  
                df = pd.DataFrame(data)
            else:  
                # handle single patient (dict)
                df = pd.DataFrame([data])

            # Show as interactive table in Streamlit
            st.dataframe(df, use_container_width=True)
            print(response.status_code)
            print(response.text)
            

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to API. Make sure the backend is running.")
# end statistic section --------------------------------------        
