import streamlit as st
import requests
import pandas as pd

# ---------- Function: Show Patients Descriptive Statistics ----------
def show_statistics():
    """
    Fetch and display patients' descriptive statistics from the API in an interactive table.

    This function performs the following steps:
    1. Sends a GET request to the API endpoint `/stats/`.
    2. Converts the returned JSON data into a pandas DataFrame.
    3. Removes the DataFrame index for a cleaner display.
    4. Displays the data interactively in Streamlit.
    5. Handles connection errors or other exceptions gracefully.

    Returns:
        None

    Raises:
        requests.exceptions.ConnectionError: If the API cannot be reached.
        Exception: Any other errors during data retrieval or display.

    Example:
        >>> show_statistics()
        Fetches patient statistics from the API and shows them in a Streamlit interactive table.
    """
    st.subheader("Patients Descriptive Statistics")
    
    BASE_URL = "http://127.0.0.1:8000"
    url = f"{BASE_URL}/stats/"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # Convert JSON to DataFrame
        if isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            df = pd.DataFrame([data])
        
        # Remove index column for display
        df_display = df.reset_index(drop=True)
        
        # Display interactive table in Streamlit
        st.dataframe(df_display, use_container_width=True)
        
        print(response.status_code)
        print(response.text)
        
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to API. Make sure the backend is running.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# ---------- Run the function ----------
show_statistics()
