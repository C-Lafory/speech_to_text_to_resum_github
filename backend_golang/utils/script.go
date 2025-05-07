package utils

import (
	"fmt"
	"os"
	"os/exec"
)

// Transcription appelle le script Python pour générer la transcription.
func Transcription(uuid string) bool {
	pythonEnv := "./speech_to_text/venv/bin/python3"
	scriptPath := "./speech_to_text/transcription.py"

	args := []string{scriptPath, uuid}
	cmd := exec.Command(pythonEnv, args...)

	// Pour debug en local
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	if err := cmd.Run(); err != nil {
		fmt.Printf("❌ Transcription error: %v\n", err)
		return false
	}
	return true
}

// Resume appelle le script Python qui résume la transcription.
func Resume(uuid string) bool {
	pythonEnv := "./speech_to_text/venv/bin/python3"
	scriptPath := "./speech_to_text/resume.py"

	args := []string{scriptPath, uuid}
	cmd := exec.Command(pythonEnv, args...)

	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	if err := cmd.Run(); err != nil {
		fmt.Printf("❌ Résumé error: %v\n", err)
		return false
	}
	return true
}

// GenerateResumeAudio appelle le script Python qui synthétise le résumé.
func GenerateResumeAudio(uuid string) bool {
	pythonEnv := "./speech_to_text/venv310/bin/python3"
	scriptPath := "./speech_to_text/text_to_speech.py"

	args := []string{scriptPath, uuid}
	cmd := exec.Command(pythonEnv, args...)

	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	if err := cmd.Run(); err != nil {
		fmt.Printf("❌ Audio résumé error: %v\n", err)
		return false
	}
	return true
}
