# 🏥 Migration de données médicales vers MongoDB

Ce projet a pour objectif d'automatiser la **migration d’un fichier CSV de données médicales** vers une base de données **MongoDB**, dans le cadre d’une mission pour l’entreprise fictive **DataSoluTech**.

L’objectif est de prendre un fichier tabulaire (CSV) contenant des informations d’hospitalisation et de le transformer en un **modèle NoSQL optimisé**, structuré par patient et prêt pour une architecture Big Data (scalabilité horizontale, flexibilité du schéma, automatisation).

---

## 🔧 1. Architecture générale

La migration suit le pipeline suivant :

1. **Source** → un fichier CSV (`data/healthcare_dataset.csv`)
2. **Service Migrator (Python)** :
   - lit le CSV  
   - transforme les lignes en documents NoSQL regroupés par patient  
   - insère les documents dans MongoDB  
   - crée des index pour optimiser les requêtes  
3. **Destination** → MongoDB (conteneur Docker)  
   - Base : `medicaldb`  
   - Collection : `patients`

Toute l’architecture est désormais **conteneurisée via Docker & Docker Compose**, ce qui garantit une exécution reproductible, portable et indépendante de l’environnement machine.

---

## 📦 2. Prérequis

Avant d’utiliser le projet :

- **Docker** (obligatoire)
- **Docker Compose** (inclus dans Docker Desktop)
- Optionnel : **MongoDB Compass** pour visualiser les données après migration

Aucune installation de Python ou MongoDB sur ton ordinateur n’est nécessaire :  
➡️ **Tout tourne dans les conteneurs Docker.**

---

## 📁 3. Structure du projet

```bash
medical_migration/
│
├── data/
│   └── healthcare_dataset.csv            # Fichier CSV source
│
├── migration/
│   ├── migrate.py                        # Script de migration (CSV → MongoDB)
│   ├── requirements.txt                  # Dépendances Python
│   └── Dockerfile                        # Image Docker du Migrator
│
├── mongo/
│   └── init-mongo.js                     # Script d'initialisation : création user & DB
│
├── docker-compose.yml                    # Orchestration des conteneurs
├── .env                                  # Variables locales (optionnel)
└── README.md




