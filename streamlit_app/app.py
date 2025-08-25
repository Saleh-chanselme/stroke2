import streamlit as st
import requests
import pandas as pd
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder
import matplotlib as plt
import plotly.express as px
import json
from st_social_media_links import SocialMediaIcons



# Make the entire app full width
st.set_page_config(layout="wide") 
    


# App title 
st.title("Welcome to :red[Stroke] dataset")

# setting the tabs (nav bar)
home, data, visualization, statistics = st.tabs(["Home", "Data", "Visualization", "Statistics"])

# start home section 
with home:
    st.header("Stroke Data Analysis App")
    st.markdown("""Interactive web app that :red[visualizes] and :red[analyzes] patient data related to :red[__stroke__.]
Purpose: To explore stroke-related factors and present insights through clear visualizations.""")
# end home section 


# start data section ------------------------
with data:
    # section header 
    st.subheader("Patient Informations Form :")

    # Form 1: Search by ID
    with st.form("id_form"):
        st.caption("Search Patient By :red[__Id__]")
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
        gender = st.radio("Select Gender:",("Male", "Female", "Other"), horizontal=True)
        stroke = st.radio("Filter by Stroke:",("No", "Yes"),horizontal=True)
        # Convert to "0"/"1" if needed
        stroke = "1" if stroke == "Yes" else "0"


        max_age = age = st.slider("Select Age", 0, 100, 25)
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
                    AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=False, fit_columns_on_grid_load=True)
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

with st.sidebar:
    #st.header("Settings")
    info, contact , support = st.tabs(["Info", "Contact us", "Help Center"])
    with info:
        st.subheader("Stroke Data Application")
        st.markdown("""
                    This application is designed to :
Explore and visualize patient stroke data, 
filter by ID, gender, or age, 
and uncover key risk factors via FastAPI.


Designed and developed by:
- Saleh Chanselme
- Chaima Haddad
                    
                    """)
        
        
    with contact:
            st.subheader("Drop Us A Line !")

            social_media_links = [
                "https://www.facebook.com",
                "https://www.youtube.com",
                "https://www.instagram.com",
                "https://github.com/Saleh-chanselme",
            ]

            social_media_icons = SocialMediaIcons(social_media_links)

            social_media_icons.render()
            
            
    with support:
        st.markdown('''
                    
                    If you have any questions, feedback, or encounter any issues while using the Stroke Project application, 
                    we’re here to help.
                    You can reach us through:
                    ''')
        st.write("	Email: saleh.chanselme@gmail.com")
        st.write("	Email: chaimaabdraouf@gmail.com")
        
        


# start footer ------------------------
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        left:0;
        width: 100%;
        background-color: #f8f9fa;
        color: #333;
        text-align: center;
        font-size: 14px;
    }
    .footer p {
                font-weight: 700;

    }
    .footer span {
        color: #B50000;
    }
        .footer span.simplon {
        font-size : 20px
    }
    </style>

    <div class="footer">
        <p>© 2025 <span class="simplon">SIMPLON</span> Formation Centre – <span>Saleh CHANSELME</span>. All rights reserved.</p>
        <p>This app is for educational purposes only and does not provide medical advice.</p>
    </div>
    """,
    unsafe_allow_html=True
)
# end footer ---------------------