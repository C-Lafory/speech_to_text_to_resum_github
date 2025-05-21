package models

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

// AudioInfos représente les informations du fichier audio
type AudioInfos struct {
	Filename string // Nom du fichier d'origine
}

// SaveAudioFileWithUUID enregistre l'audio dans un dossier dédié : ./api/file/user_<id>/<uuid>/audio.wav
func SaveAudioFileWithUUID(userID int, audioUUID string, file AudioInfos) (string, string, error) {
	// Extraire l'extension du fichier d'origine
	safeFilename := strings.ReplaceAll(file.Filename, " ", "_")
	audioExt := filepath.Ext(safeFilename) // ex: .wav, .mp3

	// 📁 Répertoire final : ./api/files/user_<id>/<uuid>/
	targetDir := fmt.Sprintf("./api/files/user_%d/%s", userID, audioUUID)
	if err := os.MkdirAll(targetDir, os.ModePerm); err != nil {
		return "", "", fmt.Errorf("could not create target dir: %w", err)
	}

	// 📄 Nom du fichier audio dans le dossier : audio.wav / audio.mp3...
	audioFilename := "audio" + audioExt
	audioPath := filepath.Join(targetDir, audioFilename)

	// ✅ Retourner les chemins
	absPath := audioPath                             // pour traitement
	dbPath := strings.TrimPrefix(audioPath, "./api") // pour BDD
	return absPath, dbPath, nil
}
