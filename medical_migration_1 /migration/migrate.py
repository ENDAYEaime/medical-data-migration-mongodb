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

# =========================
# UTILITAIRES
# =========================

def create_patient_id(name, birth_year=None):
    """Créer un identifiant unique à partir du nom et de l’année."""
    clean_name = name.replace(" ", "_").lower()
    return f"patient_{clean_name}_{birth_year if birth_year else 'unknown'}"

# =========================
# CHARGEMENT CSV
# =========================

def load_csv(file_path):
    """Charge le fichier CSV."""
    print(f"Chargement du fichier CSV : {file_path}")
    return pd.read_csv(file_path)

# =========================
# TESTS AVANT MIGRATION
# =========================

def test_csv_integrity(df):
    """Tests d'intégrité automatiques sur le CSV (avant migration)."""

    print("Tests d'intégrité AVANT migration (CSV)...")

    required_columns = [
        "Name", "Age", "Gender", "Blood Type",
        "Medical Condition", "Date of Admission",
        "Doctor", "Hospital"
    ]

    # Colonnes obligatoires
    for col in required_columns:
        assert col in df.columns, f"Colonne manquante : {col}"

    # Valeurs manquantes critiques
    assert df[required_columns].isnull().sum().sum() == 0, \
        "Valeurs manquantes détectées dans le CSV"

    # Types
    assert pd.api.types.is_numeric_dtype(df["Age"]), \
        "La colonne Age doit être numérique"

    # Doublons patients (proxy : Name + Age)
    assert not df.duplicated(subset=["Name", "Age"]).any(), \
        "Doublons patients détectés"

    print("✔ Tests CSV OK")

# =========================
# TRANSFORMATION
# =========================

def transform_data(df):
    """Transforme les données CSV en documents MongoDB (orientés patient)."""

    patients = {}

    for _, row in df.iterrows():
        name = row["Name"]
        age = row["Age"]
        birth_year = datetime.now().year - age
        pid = create_patient_id(name, birth_year)

        if pid not in patients:
            patients[pid] = {
                "_id": pid,
                "name": name,
                "age": int(age),
                "gender": row["Gender"],
                "blood_type": row["Blood Type"],
                "admissions": []
            }

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

# =========================
# INSERTION MONGODB
# =========================

def insert_into_mongo(documents):
    """Insère les documents dans MongoDB."""

    print("Connexion à MongoDB...")
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Nettoyage avant import
    collection.delete_many({})

    print(f"Insertion de {len(documents)} documents...")
    collection.insert_many(documents)

    # Index
    collection.create_index({"name": 1})
    collection.create_index({"admissions.medical_condition": 1})

    print("✔ Insertion MongoDB terminée")

# =========================
# TESTS APRES MIGRATION
# =========================

def test_mongo_integrity(expected_count):
    """Tests d'intégrité automatiques sur MongoDB (après migration)."""

    print("Tests d'intégrité APRÈS migration (MongoDB)...")

    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Nombre de documents
    mongo_count = collection.count_documents({})
    assert mongo_count == expected_count, \
        "Mismatch entre le nombre de documents MongoDB et le CSV"

    # Structure minimale des documents
    sample_doc = collection.find_one()
    required_fields = ["_id", "name", "age", "gender", "admissions"]

    for field in required_fields:
        assert field in sample_doc, \
            f"Champ manquant dans MongoDB : {field}"

    print("✔ Tests MongoDB OK")

# =========================
# MAIN
# =========================

def main():
    # Charger les données
    df = load_csv(DATA_FILE)

    # Tests AVANT migration
    test_csv_integrity(df)

    # Transformation
    documents = transform_data(df)

    # Insertion MongoDB
    insert_into_mongo(documents)

    # Tests APRES migration
    test_mongo_integrity(len(documents))

    print("Migration et tests terminés avec succès")

if __name__ == "__main__":
    main()


