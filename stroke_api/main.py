from fastapi import FastAPI
import pandas as pd
import numpy as np
from stroke_api.api import router

# Création d'un objet FastAPI
app = FastAPI(title="Stroke Dataset API")

# Inclusion des routes définies dans api.py
app.include_router(router)
