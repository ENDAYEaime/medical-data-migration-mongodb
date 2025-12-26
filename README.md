# medical-data-migration-mongodb
Migration de données médicales MongoDB

Ce projet a pour objectif de migrer un jeu de données médicales depuis un fichier CSV vers une base de données MongoDB, en mettant en place une solution automatisée, portable et scalable grâce à Docker.
Une étude des options de déploiement sur le cloud AWS est également réalisée afin de proposer une architecture adaptée aux besoins du client.

## Objectifs du projet

Migrer des données médicales depuis un fichier CSV vers MongoDB

Automatiser la migration à l’aide d’un script Python

Conteneuriser la solution avec Docker et Docker Compose

Mettre en place l’authentification et la gestion des accès MongoDB

Étudier les solutions de déploiement MongoDB sur AWS

## Structure du projet

medical-data-migration-mongodb/
│
├── data/
│   └── healthcare_dataset.csv
│
├── migration/
│   ├── migrate.py
│   ├── crud_demo.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── mongo/
│   └── init-mongo.js
│
├── .env
├── .gitignore
├── .gitattributes
│
├── docker-compose.yml
└── README.md



## Technologies utilisées

Python

MongoDB

Docker & Docker Compose

AWS (étude de déploiement)

## Lancement du projet (local)

Cloner le repository

Se placer à la racine du projet

Lancer les conteneurs avec Docker Compose :

docker-compose up --build


La migration des données est alors exécutée automatiquement et les données sont insérées dans MongoDB.

## Déploiement sur AWS

Une étude comparative des solutions AWS a été réalisée, notamment :

Amazon DocumentDB (compatible MongoDB)

MongoDB déployé sur Amazon ECS

La solution Amazon DocumentDB est recommandée pour ce client afin de réduire la charge opérationnelle et simplifier la maintenance.

## Contexte pédagogique

Ce projet a été réalisé dans le cadre d’un projet de formation Data Engineering, avec pour objectif de démontrer la capacité à :

concevoir une architecture data scalable

automatiser une migration de données

justifier des choix techniques et cloud
