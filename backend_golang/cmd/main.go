package main

import (
	"errors"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/exec"

	"api/database"
	"api/handlers"
	"api/middleware"
)

const PORT = ":5050"

func main() {
	// Initialisation base de données
	database.InitDB()
	defer database.DB.Close()

	// Chargement éventuel des modèles Python
	initPythonModels()

	// Initialisation du routeur
	router := setupRoutes()

	// Démarrage serveur
	fmt.Printf("📡 Serveur en cours sur http://localhost%s\n", PORT)
	if err := http.ListenAndServe(PORT, router); err != nil {
		log.Fatalf("Erreur lancement serveur : %v", err)
	}
}

func initPythonModels() {
	if _, err := os.Stat("models/"); errors.Is(err, os.ErrNotExist) {
		fmt.Println("📥 Modèles non trouvés. Téléchargement en cours...")

		commands := [][]string{
			{"./backend_python/venv312/bin/python3", "./backend_python/init_models.py"},
			{"./backend_python/venv310/bin/python3", "./backend_python/init_models.py"},
		}

		for _, cmdArgs := range commands {
			cmd := exec.Command(cmdArgs[0], cmdArgs[1])
			cmd.Stdout = os.Stdout
			cmd.Stderr = os.Stderr
			if err := cmd.Run(); err != nil {
				log.Fatalf("❌ Erreur d'exécution du script Python %s : %v", cmdArgs[1], err)
			}
		}

		fmt.Println("✅ Modèles Python téléchargés.")
	}
}

func setupRoutes() http.Handler {
	mux := http.NewServeMux()

	// 📁 Routes statiques (accès aux fichiers générés)
	mux.Handle("/file/", http.StripPrefix("/file", http.FileServer(http.Dir("static/file"))))
	mux.Handle("/audio/", http.StripPrefix("/audio", http.FileServer(http.Dir("static/upload/audio"))))

	// 📦 Endpoints API - Audio / Traitement
	mux.Handle("/api/audio", middleware.AuthMiddleware(database.DB)(handlers.HandlerNewAudio(database.DB)))

	// 🔐 Authentification
	mux.Handle("/api/register", middleware.RateLimitIP(handlers.HandlerRegister(database.DB)))
	mux.Handle("/api/login", middleware.RateLimitIP(handlers.HandlerLogin(database.DB)))

	// Exemple d'endpoint protégé à venir :
	// mux.Handle("/api/files", middleware.AuthMiddleware(database.DB)(handlers.HandleGetFiles(database.DB)))

	return mux
}
