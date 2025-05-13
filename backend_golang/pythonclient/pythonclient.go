package pythonclient

import (
	"bytes"
	"encoding/json"
	"io"
	"mime/multipart"
	"net/http"
	"os"
)

const (
	baseURL = "http://backend_python:8000"
	apiKey  = "sk-internal-backend-python-1234" // Doit correspondre à ton .env Python
)

func Transcribe(filePath string) (string, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return "", err
	}
	defer file.Close()

	body := &bytes.Buffer{}
	writer := multipart.NewWriter(body)
	part, _ := writer.CreateFormFile("audio_file", "audio.wav")
	io.Copy(part, file)
	writer.Close()

	req, _ := http.NewRequest("POST", baseURL+"/transcribe", body)
	req.Header.Set("x-api-key", apiKey)
	req.Header.Set("Content-Type", writer.FormDataContentType())

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	var result struct {
		Transcription string `json:"transcription"`
	}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return "", err
	}
	return result.Transcription, nil
}

func Summarize(text string) (string, error) {
	payload := map[string]string{"text": text}
	jsonData, _ := json.Marshal(payload)

	req, _ := http.NewRequest("POST", baseURL+"/summarize", bytes.NewBuffer(jsonData))
	req.Header.Set("x-api-key", apiKey)
	req.Header.Set("Content-Type", "application/json")

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	var result struct {
		Summary string `json:"summary"`
	}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return "", err
	}
	return result.Summary, nil
}

func Speak(text string, outputPath string) error {
	payload := map[string]string{"text": text}
	jsonData, _ := json.Marshal(payload)

	req, _ := http.NewRequest("POST", "http://tts_service:8001/speak", bytes.NewBuffer(jsonData))
	req.Header.Set("x-api-key", apiKey)
	req.Header.Set("Content-Type", "application/json")

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	out, err := os.Create(outputPath)
	if err != nil {
		return err
	}
	defer out.Close()
	_, err = io.Copy(out, resp.Body)
	return err
}
