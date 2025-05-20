package handlers

import (
	"database/sql"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"time"

	database "api/database/queries"
	"api/middleware"
	"api/pkg/models"
	"api/utils"

	"api/pythonclient"

	"github.com/google/uuid"
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

		// Parse multipart form
		err := r.ParseMultipartForm(10 << 20) // 10 MB max
		if err != nil {
			utils.RespondWithMessage(w, http.StatusBadRequest, "Error parsing form")
			return
		}

		// Get file from form
		file, handler, err := r.FormFile("file")
		if err != nil {
			utils.RespondWithMessage(w, http.StatusBadRequest, "Error retrieving file")
			return
		}
		defer file.Close()

		// Create audio info
		audioinfo := models.AudioInfos{
			Filename: handler.Filename,
		}

		audioUUID := uuid.NewString()
		absPath, dbPath, err := models.SaveAudioFileWithUUID(userID, audioUUID, audioinfo)
		if err != nil {
			utils.RespondWithMessage(w, http.StatusInternalServerError, fmt.Sprintf("Error saving audio: %v", err))
			return
		}

		// Create destination file
		dst, err := os.Create(absPath)
		if err != nil {
			utils.RespondWithMessage(w, http.StatusInternalServerError, "Error creating file")
			return
		}
		defer dst.Close()

		// Copy file content
		if _, err := io.Copy(dst, file); err != nil {
			utils.RespondWithMessage(w, http.StatusInternalServerError, "Error saving file")
			return
		}

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
		os.WriteFile(transPath, []byte(transcription), 0o644)

		// 2. Résumé
		summary, err := pythonclient.Summarize(transcription)
		if err != nil {
			utils.RespondWithMessage(w, http.StatusInternalServerError, "Résumé failed")
			return
		}
		os.WriteFile(summaryPath, []byte(summary), 0o644)

		// 3. TTS
		err = pythonclient.Speak(summary, audioOutPath)
		if err != nil {
			utils.RespondWithMessage(w, http.StatusInternalServerError, "Audio résumé generation failed")
			return
		}

		// 💾 Enregistrement DB
		fileRecord := models.File{
			UserID:            userID,
			AudioInputPath:    dbPath,
			TranscriptionPath: strings.TrimPrefix(transPath, "./static"),
			SummaryPath:       strings.TrimPrefix(summaryPath, "./static"),
			AudioOutputPath:   strings.TrimPrefix(audioOutPath, "./static"),
			CreatedAt:         time.Now(),
		}
		if err := database.InsertFileRecord(db, &fileRecord); err != nil {
			utils.RespondWithMessage(w, http.StatusInternalServerError, "Error saving file in DB")
			return
		}

		// ✅ Réponse
		utils.RespondWithJSON(w, http.StatusOK, map[string]interface{}{
			"message":     "Audio processed successfully.",
			"transcript":  fileRecord.TranscriptionPath,
			"summary":     fileRecord.SummaryPath,
			"audio_final": fileRecord.AudioOutputPath,
		})
	}
}
