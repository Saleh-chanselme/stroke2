from fastapi import APIRouter, HTTPException
# Import the custom filters module from your stroke_api package
from stroke_api import filters  

# Create an API router instance
router = APIRouter()

# Root endpoint: basic welcome message
@router.get("/")
def read_root():
    """
    Returns a simple welcome message for the API.
    """
    return {"message": "Bienvenue sur l'API Stroke Prediction !"}


# Endpoint to get patients, with optional filters
@router.get("/patients/")
def get_patients(
    gender: str = None,   # Optional filter for patient gender
    stroke: int = None,   # Optional filter for stroke status (0 or 1)
    max_age: float = None # Optional filter for maximum age
):
    """
    Retrieve patients with optional filters applied.
    Uses the filter_patient function from filters module.
    """
    try:
        # Call the filter function to get filtered patient DataFrame
        filtered_df = filters.filter_patient(gender=gender, stroke=stroke, max_age=max_age)
        return filtered_df  # Return the filtered data
    except Exception:
        # Raise HTTP 404 if any error occurs during filtering
        raise HTTPException(status_code=404, detail="n")


# Endpoint to get a single patient by ID
@router.get("/patients/{patient_id}")
def get_patient_id(patient_id: int):
    """
    Retrieve a patient's information by their ID.
    Handles the case where the ID does not exist.
    """
    # Call function to get patient info
    id_df = filters.get_info_by_id(patient_id)
    
    # If no patient found or the DataFrame is empty, return 404
    if id_df is None or (hasattr(id_df, 'empty') and id_df.empty):
        raise HTTPException(status_code=404, detail="Patient ID not found")

    return id_df  # Return the patient's info


# Endpoint to get basic statistics on the patient dataset
@router.get("/stats/")
def get_stats():
    """
    Calculate and return key statistics about the patient dataset:
    - Total number of patients
    - Average age
    - Average stroke rate
    - Average hypertension and heart disease prevalence
    - Average, minimum, maximum glucose levels
    - Average BMI
    """
    # Make a copy of the dataset to avoid modifying the original
    df = filters.stroke_data_df.copy()
    try:
        stats = {
            "Total_patients": int(df['id'].count()),  # Count of patients
            "Average_age": float(df['age'].mean().round(2)),  # Mean age
            "Average_stroke": float(df['stroke'].mean().round(2)),  # Mean stroke rate
            "Average_hypertension": float(df['hypertension'].mean().round(2)),  # Mean hypertension
            "Average_heart_disease": float(df['heart_disease'].mean().round(2)),  # Mean heart disease
            "Average_glucose_level": int(df['avg_glucose_level'].mean().round(3)),  # Mean glucose
            "Minimum_glucose_level": int(df['avg_glucose_level'].min().round(3)),  # Minimum glucose
            "Maximum_glucose_level": int(df['avg_glucose_level'].max().round(3)),  # Maximum glucose
            "Average_bmi": int(df['bmi'].mean())  # Mean BMI
        }
    except Exception:
        # Raise HTTP 404 if any error occurs while calculating stats
        raise HTTPException(status_code=404, detail="")

    return stats  # Return the statistics dictionary
