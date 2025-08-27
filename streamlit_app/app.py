import streamlit as st
import requests
import pandas as pd
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder
import matplotlib as plt
import plotly.express as px
import json
from st_social_media_links import SocialMediaIcons




# App title 
st.title("Welcome to :red[Stroke] dataset")

pg = st.navigation([st.Page("pages/Home.py"), st.Page("pages/Data.py"), st.Page("pages/Visualization.py"),
                    st.Page("pages/Statistics.py")])
pg.run()




# Make the entire app full width
st.set_page_config(layout="wide") 

with st.sidebar:
    st.header("About This App")
    info, contact , support = st.tabs(["Info", "Contact us", "Help Center"])
    with info:
        st.subheader("This Application Is :")
        st.markdown("""
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