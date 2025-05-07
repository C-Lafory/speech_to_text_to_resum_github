package database

import (
	"database/sql"
	"errors"
	"time"

	"api/pkg/models"
)

// GetUserByUsername récupère un utilisateur par son nom d'utilisateur
func GetUserByUsername(db *sql.DB, username string) (*models.UserInfos, error) {
	var user models.UserInfos
	query := "SELECT id, password FROM users WHERE username = ?"
	err := db.QueryRow(query, username).Scan(&user.ID, &user.Password)
	if err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return nil, errors.New("user not found")
		}
		return nil, err
	}
	return &user, nil
}

// CreateUser insère un nouvel utilisateur dans la base de données
func CreateUser(db *sql.DB, user *models.UserInfos) error {
	query := "INSERT INTO users (username, password, email) VALUES (?, ?, ?)"
	_, err := db.Exec(query, user.Username, user.Password, user.Email)
	return err
}

func CreateSession(db *sql.DB, userID int, tokenHash string, expiresAt time.Time) error {
	query := "INSERT INTO sessions (user_id, token, expires_at) VALUES (?, ?, ?)"
	_, err := db.Exec(query, userID, tokenHash, expiresAt)
	return err
}

// GetSessionByToken récupère une session par son token
func GetSessionByToken(db *sql.DB, token string) (*models.Session, error) {
	var session models.Session
	query := "SELECT id, user_id FROM sessions WHERE token = ?"
	err := db.QueryRow(query, token).Scan(&session.ID, &session.UserID)
	if err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return nil, errors.New("session not found")
		}
		return nil, err
	}
	return &session, nil
}

// DeleteSession supprime une session de la base de données
func DeleteSession(db *sql.DB, token string) error {
	query := "DELETE FROM sessions WHERE token = ?"
	_, err := db.Exec(query, token)
	return err
}

// GetUserByID récupère un utilisateur par son ID
func GetUserByID(db *sql.DB, userID int) (*models.UserInfos, error) {
	var user models.UserInfos
	query := "SELECT id, username, email FROM users WHERE id = ?"
	err := db.QueryRow(query, userID).Scan(&user.ID, &user.Username, &user.Email)
	if err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return nil, errors.New("user not found")
		}
		return nil, err
	}
	return &user, nil
}

// UpdateUser met à jour les informations d'un utilisateur
func UpdateUser(db *sql.DB, user *models.UserInfos) error {
	query := "UPDATE users SET username = ?, email = ? WHERE id = ?"
	_, err := db.Exec(query, user.Username, user.Email, user.ID)
	return err
}

// DeleteUser supprime un utilisateur de la base de données
func DeleteUser(db *sql.DB, userID int) error {
	query := "DELETE FROM users WHERE id = ?"
	_, err := db.Exec(query, userID)
	return err
}

// CheckUserExists vérifie si un utilisateur existe déjà avec le même username ou email
func CheckUserExists(db *sql.DB, username, email string) (bool, error) {
	var count int
	query := "SELECT COUNT(*) FROM users WHERE username = ? OR email = ?"
	err := db.QueryRow(query, username, email).Scan(&count)
	if err != nil {
		return false, err
	}
	return count > 0, nil
}

func GetSessionByHashedToken(db *sql.DB, hashedToken string) (*models.Session, error) {
	var session models.Session
	query := "SELECT id, user_id, expires_at FROM sessions WHERE token = ?"
	err := db.QueryRow(query, hashedToken).Scan(&session.ID, &session.UserID, &session.ExpiresAt)
	if err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return nil, errors.New("session not found")
		}
		return nil, err
	}
	return &session, nil
}

// DeleteExpiredSessions supprime toutes les sessions expirées
func DeleteExpiredSessions(db *sql.DB) error {
	_, err := db.Exec("DELETE FROM sessions WHERE expires_at < NOW()")
	return err
}

// InsertFileRecord insère un nouveau fichier traité dans la table files.
func InsertFileRecord(db *sql.DB, file *models.File) error {
	query := `
		INSERT INTO files (user_id, audio_input, transcription_path, summary_path, audio_output_path, created_at)
		VALUES (?, ?, ?, ?, ?, ?)
	`
	_, err := db.Exec(query,
		file.UserID,
		file.AudioInputPath,
		file.TranscriptionPath,
		file.SummaryPath,
		file.AudioOutputPath,
		file.CreatedAt,
	)
	return err
}
