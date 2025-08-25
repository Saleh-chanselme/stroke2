from typing import Optional
import pandas as pd
import numpy as np
# Chargement des données (une fois)
stroke_data_df = pd.read_parquet("stroke_api/data/clean_health.parquet")


# function that gets patients info by (stroke, gender and age) filters
def filter_patient(
    gender: Optional[str] = None,
    stroke: Optional[int] = None,
    max_age: Optional[int] = None
):

    df = stroke_data_df.copy()
    
    if stroke is not None :
        df = df.loc[df['stroke'] == stroke ]
    if gender is not None :
        df = df.loc[df['gender'] == gender]
    if max_age is not None : 
        df = df.loc[df['age'] <= max_age]
        

    return df.to_dict(orient='records')



# function to get patient info by his ID 
def get_info_by_id(patient_id: int):
    
    df = stroke_data_df.copy()
    
    if patient_id is not None:
        
        df = df.loc[df['id'] == patient_id]
        
    return df.to_dict(orient='records')


