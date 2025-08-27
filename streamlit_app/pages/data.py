import streamlit as st
import requests
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

# ---------- Global Config ----------
BASE_URL = "http://127.0.0.1:8000"

# ---------- Function 1: Search Patient by ID ----------
def get_patient_id():
    """
    Search for a patient by their ID and display the results in an interactive DataFrame.

    This function performs the following steps:
    1. Displays a form to enter a Patient ID.
    2. Sends a GET request to the API endpoint `/patients/{patient_id}`.
    3. Converts the JSON response into a pandas DataFrame.
    4. Displays the DataFrame interactively in Streamlit.
    5. Handles errors such as empty input, no matching patient, or API connection issues.

    Returns:
        None

    Raises:
        requests.exceptions.ConnectionError: If the API cannot be reached.
        Exception: Any other errors during data retrieval.

    Example:
        >>> get_patient_id()
        Displays a form to search a patient by ID and shows the patient data if found.
    """
    st.subheader("Patient Informations Form :")
    
    with st.form("id_form"):
        st.caption("Search Patient By :red[__Id__]")
        patient_id = st.text_input("Patient ID")
        submit_id = st.form_submit_button("Search")
        
    if submit_id:
        if not patient_id:
            st.info("Please enter a Patient ID to search.")
            return
        
        url = f"{BASE_URL}/patients/{patient_id}"
        try:
            response = requests.get(url)
            if response.status_code != 200:
                st.error(f"Error: {response.status_code} - {response.text}")
                return
            
            data = response.json()
            
            # Convert JSON to DataFrame
            if isinstance(data, list):
                df = pd.DataFrame(data)
            else:
                df = pd.DataFrame([data])
            
            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No patient found with this ID.")
        
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to API. Make sure the backend is running.")

# ---------- Function 2: Filter Patients ----------
def patient_filters():
    """
    Filter patients by gender, stroke status, and maximum age, and display results interactively.

    This function performs the following steps:
    1. Displays a form with options to select Gender, Stroke status, and Maximum Age.
    2. Sends a GET request to the API endpoint `/patients/` with filter parameters.
    3. Converts the JSON response into a pandas DataFrame.
    4. Displays the filtered data interactively using AgGrid.
    5. Handles errors such as no matching data or API connection issues.

    Returns:
        None

    Raises:
        requests.exceptions.ConnectionError: If the API cannot be reached.
        Exception: Any other errors during data retrieval or grid setup.

    Example:
        >>> patient_filters()
        Shows a form for filtering patients and displays the filtered data in a table.
    """
    st.subheader("Patients Filters")
    
    with st.form("filter_form"):
        gender = st.radio("Select Gender:", ("Male", "Female", "Other"), horizontal=True)
        stroke = st.radio("Filter by Stroke:", ("No", "Yes"), horizontal=True)
        stroke_val = 1 if stroke == "Yes" else 0
        max_age = st.slider("Select Maximum Age", 0, 100, 25)
        submit_filter = st.form_submit_button("Search")
    
    if submit_filter:
        params = {
            "gender": gender,
            "stroke": stroke_val,
            "max_age": max_age
        }
        
        url = f"{BASE_URL}/patients/"
        try:
            response = requests.get(url, params=params)
            if response.status_code != 200:
                st.error(f"Error: {response.status_code} - {response.text}")
                return
            
            data = response.json()
            
            # Convert JSON to DataFrame
            if isinstance(data, list):
                df = pd.DataFrame(data)
            else:
                df = pd.DataFrame([data])
            
            if not df.empty:
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

# ---------- Run Functions ----------
get_patient_id()
patient_filters()
