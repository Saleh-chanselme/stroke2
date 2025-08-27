import streamlit as st

def show_home_section():
    """
    Display the Home section of the Stroke Data Analysis App.

    This function sets up the main landing page for the app, including:
    1. App title and introduction.
    2. Overview of the app’s purpose.
    3. Guidance for users on how to navigate the app.

    The Home section is intended to give users a clear understanding of the app’s features
    and how to interact with patient data, filters, and visualizations.

    Returns:
        None

    Example:
        >>> show_home_section()
        Displays the interactive Home page of the Stroke Data Analysis App in Streamlit.
    """
    # Section Header
    st.title("🧠 Stroke Data Analysis App")
    
    st.markdown("""
    Welcome to the **Stroke Data Analysis App**, an interactive web application that **visualizes** 
    and **analyzes** patient data related to **stroke**.

    ### Purpose:
    - Explore stroke-related factors.
    - Present insights through **clear visualizations**.
    - Filter patients by **ID, gender, or age**.
    - Uncover key risk factors via **FastAPI backend**.

    This app is designed to provide an easy-to-use interface for healthcare professionals,
    researchers, or anyone interested in stroke data analysis.
    """)
    
    st.markdown("---")
    
    st.info("Use the navigation menu to explore patient data, apply filters, and visualize statistics.")

# Call the function to display the home section
show_home_section()
