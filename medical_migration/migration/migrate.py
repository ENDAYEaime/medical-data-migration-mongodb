import os
import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime

# Charger les variables du fichier .env
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
DATA_FILE = os.getenv("DATA_FILE")

def create_patient_id(name, birth_year=None):
    """Créer un identifiant unique à partir du nom et de l’année."""
    clean_name = name.replace(" ", "_").lower()
    return f"patient_{clean_name}_{birth_year if birth_year else 'unknown'}"

def load_csv(file_path):
    """Charge n'importe quel CSV envoyé par l'entreprise."""
    print(f"Chargement du fichier CSV : {file_path}")
    return pd.read_csv(file_path)

def transform_data(df):
    """Transforme les lignes CSV en structure NoSQL regroupée par patient."""
    
    patients = {}

    for _, row in df.iterrows():
        name = row["Name"]
        age = row["Age"]
        birth_year = datetime.now().year - age  
        pid = create_patient_id(name, birth_year)

        # Initialiser un patient s'il n'existe pas
        if pid not in patients:
            patients[pid] = {
                "_id": pid,
                "name": name,
                "age": int(age),
                "gender": row["Gender"],
                "blood_type": row["Blood Type"],
                "admissions": []
            }

        # Ajouter une admission
        admission_record = {
            "medical_condition": row["Medical Condition"],
            "date_of_admission": row["Date of Admission"],
            "discharge_date": row["Discharge Date"],
            "doctor": row["Doctor"],
            "hospital": row["Hospital"],
            "room_number": row["Room Number"],
            "admission_type": row["Admission Type"],
            "medication": row["Medication"],
            "test_results": row["Test Results"],
            "billing_amount": float(row["Billing Amount"]),
            "insurance_provider": row["Insurance Provider"]
        }

        patients[pid]["admissions"].append(admission_record)

    return list(patients.values())

def insert_into_mongo(documents):
    """Insère les documents dans MongoDB."""
    
    print("Connexion à MongoDB...")
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # vider la collection avant import (optionnel)
    collection.delete_many({})
    
    print(f"Insertion de {len(documents)} documents...")
    collection.insert_many(documents)

    print("Création des index...")
    collection.create_index({"name": 1})
    collection.create_index({"admissions.medical_condition": 1})

    print("Migration terminée avec succès !")

def main():
    df = load_csv(DATA_FILE)
    docs = transform_data(df)
    insert_into_mongo(docs)

if __name__ == "__main__":
    main()

