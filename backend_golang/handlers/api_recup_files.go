package handlers

import (
	"database/sql"
	"encoding/base64"
	"log"
	"net/http"
	"os"
	"time"

	database "api/database/queries"
	"api/middleware"
	"api/utils"
)

// Structure pour la réponse
type FileContent struct {
	Date            string `json:"date"`            // Date en string
	Transcription   string `json:"transcription"`   // Contenu de la transcription
	Summary         string `json:"summary"`         // Contenu du résumé
	AudioInputData  string `json:"audioInputData"`  // Données audio en base64
	AudioOutputData string `json:"audioOutputData"` // Données audio en base64
}

// Handler pour servir les fichiers audio
func HandlerServeAudio(db *sql.DB) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		// 🔐 Authentification via middleware
		userID, ok := r.Context().Value(middleware.UserIDKey).(int)
		if !ok || userID == 0 {
			utils.RespondWithMessage(w, http.StatusUnauthorized, "Unauthorized")
			return
		}

		// Récupérer le chemin du fichier depuis l'URL
		filePath := r.URL.Query().Get("path")
		if filePath == "" {
			utils.RespondWithMessage(w, http.StatusBadRequest, "No file path provided")
			return
		}

		// Vérifier que le fichier appartient à l'utilisateur
		file, err := database.GetFileByPath(db, filePath)
		if err != nil || file.UserID != userID {
			utils.RespondWithMessage(w, http.StatusForbidden, "Access denied")
			return
		}

		// Servir le fichier
		http.ServeFile(w, r, filePath)
	}
}

func HandlerGetUserFiles(db *sql.DB) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		log.Println("1. Début du handler GetUserFiles")
		utils.SetJSONHeaders(w)

		// 🔐 Authentification via middleware
		userID, ok := r.Context().Value(middleware.UserIDKey).(int)
		if !ok || userID == 0 {
			log.Println("2. Erreur d'authentification")
			utils.RespondWithMessage(w, http.StatusUnauthorized, "Unauthorized")
			return
		}
		log.Printf("3. Utilisateur authentifié: %d", userID)

		// 🔍 Récupération en BDD
		files, err := database.GetFilesByUserID(db, userID)
		if err != nil {
			log.Printf("4. Erreur récupération BDD: %v", err)
			utils.RespondWithMessage(w, http.StatusInternalServerError, "Error fetching files")
			return
		}
		log.Printf("5. %d fichiers trouvés en BDD", len(files))

		// 📝 Lecture du contenu des fichiers
		var fileContents []FileContent
		for i, file := range files {
			log.Printf("6. Traitement du fichier %d/%d", i+1, len(files))

			// Lecture de la transcription
			transcriptionContent, err := os.ReadFile(file.TranscriptionPath)
			if err != nil {
				log.Printf("7. Erreur lecture transcription: %v", err)
				utils.RespondWithMessage(w, http.StatusInternalServerError, "Error reading transcription file")
				return
			}

			// Lecture du résumé
			summaryContent, err := os.ReadFile(file.SummaryPath)
			if err != nil {
				log.Printf("8. Erreur lecture résumé: %v", err)
				utils.RespondWithMessage(w, http.StatusInternalServerError, "Error reading summary file")
				return
			}

			// Lecture de l'audio original
			audioInputData, err := os.ReadFile(file.AudioInput)
			if err != nil {
				log.Printf("9. Erreur lecture audio input: %v", err)
				utils.RespondWithMessage(w, http.StatusInternalServerError, "Error reading input audio file")
				return
			}

			// Lecture de l'audio du résumé
			audioOutputData, err := os.ReadFile(file.AudioOutput)
			if err != nil {
				log.Printf("10. Erreur lecture audio output: %v", err)
				utils.RespondWithMessage(w, http.StatusInternalServerError, "Error reading output audio file")
				return
			}

			// Conversion des données en base64
			audioInputBase64 := base64.StdEncoding.EncodeToString(audioInputData)
			audioOutputBase64 := base64.StdEncoding.EncodeToString(audioOutputData)

			fileContents = append(fileContents, FileContent{
				Date:            file.CreatedAt.Format(time.RFC3339),
				Transcription:   string(transcriptionContent),
				Summary:         string(summaryContent),
				AudioInputData:  audioInputBase64,
				AudioOutputData: audioOutputBase64,
			})
			log.Printf("11. Fichier %d traité avec succès", i+1)
		}

		// Définir les headers pour le streaming
		w.Header().Set("Content-Type", "application/json")
		w.Header().Set("Transfer-Encoding", "chunked")

		log.Println("12. Envoi de la réponse")
		// ✅ Réponse avec le contenu des fichiers
		utils.RespondWithJSON(w, http.StatusOK, fileContents)
		log.Println("13. Réponse envoyée avec succès")
	}
}
