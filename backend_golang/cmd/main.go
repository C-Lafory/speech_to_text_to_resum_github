package main

import (
	"fmt"
	"log"
	"net/http"

	"api/database"
	"api/handlers"
	"api/middleware"
)

const PORT = ":5048"

func main() {
	// Initialisation base de données
	database.InitDB()
	defer database.DB.Close()

	// Chargement éventuel des modèles Python
	// initPythonModels()

	// Initialisation du routeur
	router := setupRoutes()

	// Démarrage serveur
	fmt.Printf("📡 Serveur en cours sur http://localhost%s\n", PORT)
	if err := http.ListenAndServe(PORT, router); err != nil {
		log.Fatalf("Erreur lancement serveur : %v", err)
	}
}


func setupRoutes() http.Handler {
	mux := http.NewServeMux()

	// 📁 Routes statiques (accès aux fichiers générés)
	mux.Handle("/file/", http.StripPrefix("/file", http.FileServer(http.Dir("static/file"))))
	mux.Handle("/audio/", http.StripPrefix("/audio", http.FileServer(http.Dir("static/upload/audio"))))

	// 📦 Endpoints API - Audio / Traitement
	mux.Handle("/api/audio", middleware.AuthMiddleware(database.DB)(handlers.HandlerNewAudio(database.DB)))
	mux.Handle("/api/files", middleware.AuthMiddleware(database.DB)(handlers.HandlerGetUserFiles(database.DB)))

	// 🔐 Authentification
	mux.Handle("/api/register", middleware.RateLimitIP(handlers.HandlerRegister(database.DB)))
	mux.Handle("/api/login", middleware.RateLimitIP(handlers.HandlerLogin(database.DB)))

	// Exemple d'endpoint protégé à venir :
	// mux.Handle("/api/files", middleware.AuthMiddleware(database.DB)(handlers.HandleGetFiles(database.DB)))

	return mux
}
