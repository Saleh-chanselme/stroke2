import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# ---------- Function: Load Patient Data from API ----------
def load_patient_data() -> pd.DataFrame:
    """
    Fetch patient data from the API and return it as a pandas DataFrame.

    Returns:
        pd.DataFrame: Patient data fetched from API. Returns an empty DataFrame if
        the request fails or no data is found.

    Raises:
        requests.exceptions.ConnectionError: If the API is unreachable.
        Exception: Any other error during the request.
    """
    try:
        response = requests.get("http://127.0.0.1:8000/patients/")
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data if isinstance(data, list) else [data])
            return df
        else:
            st.error("Failed to fetch data from API")
            return pd.DataFrame()
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to API")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error: {e}")
        return pd.DataFrame()

# ---------- Function: Plot Stroke vs Smoking Pie Chart ----------
def plot_stroke_smoking(df: pd.DataFrame):
    """
    Plot a pie chart of smokers vs non-smokers among stroke patients.

    Args:
        df (pd.DataFrame): Patient dataset containing 'stroke' and 'smoking_status' columns.

    Behavior:
        - Filters patients who had a stroke.
        - Counts smokers vs non-smokers.
        - Displays an interactive Plotly pie chart in Streamlit.
        - Shows a warning if no stroke patients exist.
    """
    if 'stroke' in df.columns and 'smoking_status' in df.columns:
        stroke_df = df[df['stroke'] == 1]
        if not stroke_df.empty:
            stroke_smoking_counts = stroke_df['smoking_status'].apply(
                lambda x: 'Fumeur' if x != 'never smoked' else 'Non-fumeur'
            ).value_counts()
            fig = px.pie(
                names=stroke_smoking_counts.index,
                values=stroke_smoking_counts.values,
                title="Patients ayant eu un AVC : Fumeurs vs Non-fumeurs"
            )
            st.plotly_chart(fig, use_container_width=True, key="pie_smoking")
        else:
            st.warning("No stroke patients found for smoking chart.")

# ---------- Function: Plot Stroke Distribution Pie Chart ----------
def plot_stroke_distribution(df: pd.DataFrame):
    """
    Plot a pie chart showing stroke distribution in the dataset.

    Args:
        df (pd.DataFrame): Patient dataset containing 'stroke' column.

    Behavior:
        - Counts patients with and without stroke.
        - Displays an interactive Plotly pie chart in Streamlit.
    """
    if 'stroke' in df.columns:
        counts = df['stroke'].value_counts()
        counts.index = counts.index.map({0: 'Without Stroke', 1: 'With Stroke'})
        fig = px.pie(
            names=counts.index,
            values=counts.values,
            title="Stroke Distribution"
        )
        st.plotly_chart(fig)

# ---------- Function: Plot Average BMI per Stroke Status ----------
def plot_avg_bmi(df: pd.DataFrame):
    """
    Plot a bar chart of average BMI grouped by stroke status.

    Args:
        df (pd.DataFrame): Patient dataset containing 'stroke' and 'bmi' columns.

    Behavior:
        - Groups patients by stroke status and calculates average BMI.
        - Displays an interactive Plotly bar chart in Streamlit.
    """
    if 'stroke' in df.columns and 'bmi' in df.columns:
        avg_bmi = df.groupby('stroke')['bmi'].mean().reset_index()
        avg_bmi['stroke'] = avg_bmi['stroke'].map({0: 'Without Stroke', 1: 'With Stroke'})
        fig = px.bar(
            avg_bmi,
            x='stroke',
            y='bmi',
            title="Average BMI by Stroke Status",
            labels={'stroke': 'Stroke Status', 'bmi': 'Average BMI'},
            text='bmi',
            color='stroke'
        )
        st.plotly_chart(fig)

# ---------- Main Function: Display Visual Analytics ----------
def show_visual_analytics():
    """
    Display the Stroke Data Visual Analytics section in Streamlit.

    Behavior:
        - Loads patient data from API.
        - Shows warning if dataset is empty.
        - Plots three visualizations:
            1. Smokers vs non-smokers among stroke patients.
            2. Stroke distribution in the dataset.
            3. Average BMI grouped by stroke status.
    """
    st.subheader("Stroke Data Visual Analytics")
    
    df = load_patient_data()
    if df.empty:
        st.warning("No valid data available for visualization.")
        return
    
    plot_stroke_smoking(df)
    plot_stroke_distribution(df)
    plot_avg_bmi(df)

# ---------- Run the main function ----------
show_visual_analytics()
