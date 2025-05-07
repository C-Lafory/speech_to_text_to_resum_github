package handlers

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"net/http"
	"path/filepath"
	"strings"
	"time"

	database "api/database/queries"
	"api/middleware"
	"api/pkg/models"
	"api/utils"

	"github.com/google/uuid"
)

func HandlerNewAudio(db *sql.DB) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		// 🛡️ Vérification méthode POST
		if r.Method != http.MethodPost {
			utils.RespondWithMessage(w, http.StatusMethodNotAllowed, "Only POST allowed")
			return
		}
		utils.SetJSONHeaders(w)

		// 🔐 Récupérer l’ID utilisateur via le middleware
		userID, ok := r.Context().Value(middleware.UserIDKey).(int)
		if !ok || userID == 0 {
			utils.RespondWithMessage(w, http.StatusUnauthorized, "Unauthorized")
			return
		}

		// 📥 Lecture du corps de requête
		var audioinfo models.AudioInfos
		if err := json.NewDecoder(r.Body).Decode(&audioinfo); err != nil {
			utils.RespondWithMessage(w, http.StatusBadRequest, "Invalid JSON")
			return
		}

		// 🔁 Générer un ID unique pour ce traitement (dossier)
		audioUUID := uuid.NewString()

		// 📁 Enregistrer le fichier audio dans un répertoire dédié
		absPath, dbPath, err := models.SaveAudioFileWithUUID(userID, audioUUID, audioinfo)
		if err != nil {
			utils.RespondWithMessage(w, http.StatusInternalServerError, fmt.Sprintf("Error saving audio: %v", err))
			return
		}

		// 📄 Récupérer l’extension du fichier (ex: .wav)
		audioExt := filepath.Ext(absPath)

		// 🧠 Créer le nom de base : ./static/file/user_<id>/<uuid>/
		fileBase := fmt.Sprintf("./static/file/user_%d/%s", userID, audioUUID)

		// 🧠 Transcription
		if !utils.Transcription(audioUUID + "." + strings.TrimPrefix(audioExt, ".")) {
			utils.RespondWithMessage(w, http.StatusInternalServerError, "Transcription failed")
			return
		}
		transPath := filepath.Join(fileBase, "transcription.txt")

		// 📝 Résumé
		if !utils.Resume(audioUUID) {
			utils.RespondWithMessage(w, http.StatusInternalServerError, "Résumé failed")
			return
		}
		summaryPath := filepath.Join(fileBase, "resum.txt")

		// 🔊 Génération du résumé audio
		if !utils.GenerateResumeAudio(audioUUID) {
			utils.RespondWithMessage(w, http.StatusInternalServerError, "Audio résumé generation failed")
			return
		}
		audioOutPath := filepath.Join(fileBase, "audio_resume.mp3")

		// 💾 Enregistrement dans la base
		file := models.File{
			UserID:            userID,
			AudioInputPath:    dbPath,
			TranscriptionPath: strings.TrimPrefix(transPath, "./static"),
			SummaryPath:       strings.TrimPrefix(summaryPath, "./static"),
			AudioOutputPath:   strings.TrimPrefix(audioOutPath, "./static"),
			CreatedAt:         time.Now(),
		}

		if err := database.InsertFileRecord(db, &file); err != nil {
			utils.RespondWithMessage(w, http.StatusInternalServerError, "Error saving file in DB")
			return
		}

		// ✅ Réponse finale
		utils.RespondWithJSON(w, http.StatusOK, map[string]interface{}{
			"message":     "Audio processed successfully.",
			"transcript":  file.TranscriptionPath,
			"summary":     file.SummaryPath,
			"audio_final": file.AudioOutputPath,
		})
	}
}
