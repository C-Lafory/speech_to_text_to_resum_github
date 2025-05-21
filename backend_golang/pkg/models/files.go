package models

import "time"

type File struct {
	ID                int       `json:"id"`
	UserID            int       `json:"user_id"`
	AudioInput        string    `json:"audio_input"`
	TranscriptionPath string    `json:"transcription_path"`
	SummaryPath       string    `json:"summary_path"`
	AudioOutput       string    `json:"audio_output_path"`
	CreatedAt         time.Time `json:"created_at"`
}
