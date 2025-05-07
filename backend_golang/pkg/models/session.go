package models

import "time"

type Session struct {
	ID     int    `json:"id"`      // Identifiant unique de la session.
	UserID int    `json:"user_id"` // Référence à l'utilisateur (clé étrangère).
	Token  string `json:"token"`   // Token unique pour la session.
	ExpiresAt time.Time `json:"expires_at"` // Date d'expiration de la session.
}

