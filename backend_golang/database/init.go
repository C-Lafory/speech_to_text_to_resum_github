package database

import (
    "database/sql"
    "log"

    _ "github.com/go-sql-driver/mysql"
)

var DB *sql.DB

func InitDB() {
    // Chaîne de connexion pour une base de données locale
    dsn := "test:test@tcp(localhost:3306)/mydatabase?charset=utf8mb4&parseTime=True&loc=Local"

    // Initialiser la connexion
    var err error
    DB, err = sql.Open("mysql", dsn)
    if err != nil {
        log.Fatalf("Erreur de connexion à la base de données : %v", err)
    }

    // Vérifier que la connexion fonctionne
    if err := DB.Ping(); err != nil {
        log.Fatalf("Erreur lors du ping de la base de données : %v", err)
    }

    log.Println("Connexion à la base de données réussie.")
}