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
	"api/pythonclient"
)

func HandlerNewAudio(db *sql.DB) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			utils.RespondWithMessage(w, http.StatusMethodNotAllowed, "Only POST allowed")
			return
		}
		utils.SetJSONHeaders(w)

		userID, ok := r.Context().Value(middleware.UserIDKey).(int)
		if !ok || userID == 0 {
			utils.RespondWithMessage(w, http.StatusUnauthorized, "Unauthorized")
			return
		}

		var audioinfo models.AudioInfos
		if err := json.NewDecoder(r.Body).Decode(&audioinfo); err != nil {
			utils.RespondWithMessage(w, http.StatusBadRequest, "Invalid JSON")
			return
		}

		audioUUID := uuid.NewString()
		absPath, dbPath, err := models.SaveAudioFileWithUUID(userID, audioUUID, audioinfo)
		if err != nil {
			utils.RespondWithMessage(w, http.StatusInternalServerError, fmt.Sprintf("Error saving audio: %v", err))
			return
		}

		audioExt := filepath.Ext(absPath)
		fileBase := fmt.Sprintf("./static/file/user_%d/%s", userID, audioUUID)
		transPath := filepath.Join(fileBase, "transcription.txt")
		summaryPath := filepath.Join(fileBase, "resum.txt")
		audioOutPath := filepath.Join(fileBase, "audio_resume.mp3")

		// 🧠 Nouveau traitement via FastAPI
		// 1. Transcription
		transcription, err := pythonclient.Transcribe(absPath)
		if err != nil {
			utils.RespondWithMessage(w, http.StatusInternalServerError, "Transcription failed")
			return
		}
		os.WriteFile(transPath, []byte(transcription), 0644)

		// 2. Résumé
		summary, err := pythonclient.Summarize(transcription)
		if err != nil {
			utils.RespondWithMessage(w, http.StatusInternalServerError, "Résumé failed")
			return
		}
		os.WriteFile(summaryPath, []byte(summary), 0644)

		// 3. TTS
		err = pythonclient.Speak(summary, audioOutPath)
		if err != nil {
			utils.RespondWithMessage(w, http.StatusInternalServerError, "Audio résumé generation failed")
			return
		}

		// 💾 Enregistrement DB
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

		// ✅ Réponse
		utils.RespondWithJSON(w, http.StatusOK, map[string]interface{}{
			"message":     "Audio processed successfully.",
			"transcript":  file.TranscriptionPath,
			"summary":     file.SummaryPath,
			"audio_final": file.AudioOutputPath,
		})
	}
}
