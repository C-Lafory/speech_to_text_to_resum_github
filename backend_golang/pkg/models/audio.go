package models

import (
	"encoding/base64"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strings"
)

// AudioInfos représente les données reçues dans la requête.
type AudioInfos struct {
	Data     string `json:"Data"` // Contenu en base64
	Filename string `json:"Name"` // Nom du fichier d’origine (ex: audio123.wav)
	Date     string `json:"Date"` // Optionnel
	Body     []byte // Inutilisé pour l’instant
}

// SaveAudioFileWithUUID enregistre l’audio dans un dossier dédié : ./static/file/user_<id>/<uuid>/audio.wav
func SaveAudioFileWithUUID(userID int, audioUUID string, file AudioInfos) (string, string, error) {
	// Extraire l’extension du fichier d’origine
	safeFilename := strings.ReplaceAll(file.Filename, " ", "_")
	audioExt := filepath.Ext(safeFilename) // ex: .wav, .mp3

	// 📁 Répertoire final : ./static/file/user_<id>/<uuid>/
	targetDir := fmt.Sprintf("./static/file/user_%d/%s", userID, audioUUID)
	if err := os.MkdirAll(targetDir, os.ModePerm); err != nil {
		return "", "", fmt.Errorf("could not create target dir: %w", err)
	}

	// 📄 Nom du fichier audio dans le dossier : audio.wav / audio.mp3...
	audioFilename := "audio" + audioExt
	audioPath := filepath.Join(targetDir, audioFilename)

	// 🔄 Écrire le fichier sur le disque
	f, err := os.OpenFile(audioPath, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, 0o666)
	if err != nil {
		return "", "", fmt.Errorf("could not create audio file: %w", err)
	}
	defer f.Close()

	// 🔓 Décoder les données base64 (on enlève l’entête si présent)
	base64Data := file.Data
	if strings.Contains(base64Data, ",") {
		base64Data = strings.Split(base64Data, ",")[1]
	}
	decoder := base64.NewDecoder(base64.StdEncoding, strings.NewReader(base64Data))
	if _, err := io.Copy(f, decoder); err != nil {
		return "", "", fmt.Errorf("could not write audio file: %w", err)
	}

	// ✅ Retourner les chemins
	absPath := audioPath                                     // pour traitement
	dbPath := strings.TrimPrefix(audioPath, "./static")      // pour BDD
	return absPath, dbPath, nil
}
