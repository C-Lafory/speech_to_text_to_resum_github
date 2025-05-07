# File Management API

Cette API permet la gestion de fichiers tels que les images et les fichiers audio. Elle prend en charge l'upload de fichiers encodés en Base64, leur sauvegarde sur le serveur, ainsi que la fourniture de liens pour accéder aux fichiers enregistrés.

## Fonctionnalités

- **Upload de fichiers audio** :
  - Enregistrement de fichiers audio encodés en Base64.
  - Conversion du fichier audio en .wav
  - Transcription du dit fichier 
  - Generation d'un Resumer a partir de la transcription
  - Envoie de la transcription et du resumer

## Structure du projet

    ├── cmd 
    │ └── main.go # Point d'entrée de l'application. 
    ├── handlers/ # Gestion des requêtes HTTP. 
    │ ├── audio.go # Gestion des uploads de fichiers audio. 
    ├── models/ # Structures de données et logique métier. 
    │ ├── audio.go # Modèle et logique de traitement des fichiers audio. 
    ├── static/ # Contient les fichiers uploadés. 
    │ ├── file/ # Dossier pour les fichier traiter. 
    │ └── upload/ 
    │   └── audio/ # Dossier pour les fichiers audio uploadés. 
    ├── go.mod # Fichier des dépendances Go. 
    └── README.md # Documentation du projet.


## Prérequis

- [Go](https://golang.org/) version 1.20 ou supérieure.
- Un outil comme `Postman` ou `cURL` pour tester les endpoints de l'API.
- Dossier `static` avec les sous-dossiers `file` et `upload/audio` (créés automatiquement si absents).
- Dossier contenant les différents fichier python permettant la transcription et la generation du resumer.

## Installation

1. Clonez ce dépôt :
   ```bash
        git clone https://github.com/username/file-management-api.git
        cd file-management-api
    ```
2. Installez les dépendances :
    ```bash
        go mod tidy
    ```

3. Lancez le serveur :
    ```bash
        go run main.go
    ```
4. Accédez à l'API à l'adresse suivante :
    ```arduino
        http://localhost:5050/
    ```



installer : "go get golang.org/x/time/rate" C’est le package officiel de rate limiting de Go, super léger.