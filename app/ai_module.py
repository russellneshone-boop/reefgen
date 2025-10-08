# app/ai_module.py
import random

def diagnose_coral(image_path: str) -> str:
    # Dummy AI diagnosis for demo purposes
    diagnoses = [
        "Healthy",
        "Bleached",
        "Diseased",
        "Damaged",
        "Unknown"
    ]
    return random.choice(diagnoses)
