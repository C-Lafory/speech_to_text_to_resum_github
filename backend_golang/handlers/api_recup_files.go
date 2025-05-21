package handlers

import (
	"database/sql"
	"net/http"
	"os"
	"time"

	database "api/database/queries"
	"api/middleware"
	"api/utils"
)

// Structure pour la réponse
type FileContent struct {
	Date            time.Time `json:"date"`            // Date de création comme titre
	Transcription   string    `json:"transcription"`   // Contenu de la transcription
	Summary         string    `json:"summary"`         // Contenu du résumé
	AudioInputData  []byte    `json:"audioInputData"`  // Contenu audio original
	AudioOutputData []byte    `json:"audioOutputData"` // Contenu audio du résumé
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
		utils.SetJSONHeaders(w)

		// 🔐 Authentification via middleware
		userID, ok := r.Context().Value(middleware.UserIDKey).(int)
		if !ok || userID == 0 {
			utils.RespondWithMessage(w, http.StatusUnauthorized, "Unauthorized")
			return
		}

		// 🔍 Récupération en BDD
		files, err := database.GetFilesByUserID(db, userID)
		if err != nil {
			utils.RespondWithMessage(w, http.StatusInternalServerError, "Error fetching files")
			return
		}

		// 📝 Lecture du contenu des fichiers
		var fileContents []FileContent
		for _, file := range files {
			// Lecture de la transcription
			transcriptionContent, err := os.ReadFile(file.TranscriptionPath)
			if err != nil {
				utils.RespondWithMessage(w, http.StatusInternalServerError, "Error reading transcription file")
				return
			}

			// Lecture du résumé
			summaryContent, err := os.ReadFile(file.SummaryPath)
			if err != nil {
				utils.RespondWithMessage(w, http.StatusInternalServerError, "Error reading summary file")
				return
			}

			// Lecture de l'audio original
			audioInputData, err := os.ReadFile(file.AudioInputPath)
			if err != nil {
				utils.RespondWithMessage(w, http.StatusInternalServerError, "Error reading input audio file")
				return
			}

			// Lecture de l'audio du résumé
			audioOutputData, err := os.ReadFile(file.AudioOutputPath)
			if err != nil {
				utils.RespondWithMessage(w, http.StatusInternalServerError, "Error reading output audio file")
				return
			}

			fileContents = append(fileContents, FileContent{
				Date:            file.CreatedAt,
				Transcription:   string(transcriptionContent),
				Summary:         string(summaryContent),
				AudioInputData:  audioInputData,
				AudioOutputData: audioOutputData,
			})
		}

		// Définir les headers pour le streaming
		w.Header().Set("Content-Type", "application/json")
		w.Header().Set("Transfer-Encoding", "chunked")

		// ✅ Réponse avec le contenu des fichiers
		utils.RespondWithJSON(w, http.StatusOK, fileContents)
	}
}
