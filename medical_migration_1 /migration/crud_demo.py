import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Charger les variables d’environnement
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

def mongo_connection():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return db[COLLECTION_NAME]

def create_patient(collection):
    print("CREATE : ajout d’un patient")
    patient = {
        "_id": "patient_demo_001",
        "name": "John Doe",
        "age": 45,
        "gender": "Male",
        "admissions": []
    }
    collection.insert_one(patient)

def read_patient(collection):
    print("READ : lecture du patient")
    patient = collection.find_one({"_id": "patient_demo_001"})
    print(patient)

def update_patient(collection):
    print("UPDATE : modification du patient")
    collection.update_one(
        {"_id": "patient_demo_001"},
        {"$set": {"age": 46}}
    )

def delete_patient(collection):
    print("DELETE : suppression du patient")
    collection.delete_one({"_id": "patient_demo_001"})

def main():
    collection = mongo_connection()

    create_patient(collection)
    read_patient(collection)
    update_patient(collection)
    read_patient(collection)
    delete_patient(collection)

    print("CRUD MongoDB terminé avec succès")

if __name__ == "__main__":
    main()
