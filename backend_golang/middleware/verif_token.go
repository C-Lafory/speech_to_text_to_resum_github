package middleware

import (
	"context"
	"database/sql"
	"errors"
	"net/http"
	"strings"
	"time"

	database "api/database/queries"
	"api/utils"
)

// Clé de contexte pour l'ID utilisateur
type contextKey string

const UserIDKey contextKey = "userID"

// AuthMiddleware devient une fonction qui retourne un middleware
func AuthMiddleware(db *sql.DB) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			authHeader := r.Header.Get("Authorization")
			if authHeader == "" {
				utils.RespondWithMessage(w, http.StatusUnauthorized, "Missing Authorization token.")
				return
			}

			// Bearer token
			parts := strings.Split(authHeader, " ")
			if len(parts) != 2 || parts[0] != "Bearer" {
				utils.RespondWithMessage(w, http.StatusUnauthorized, "Invalid token format.")
				return
			}
			tokenRaw := parts[1]

			// Hasher le token reçu pour le comparer avec celui en base
			tokenHash := utils.HashToken(tokenRaw)

			session, err := database.GetSessionByToken(db, tokenHash)
			if err != nil {
				if errors.Is(err, sql.ErrNoRows) {
					utils.RespondWithMessage(w, http.StatusUnauthorized, "Invalid or expired session.")
					return
				}
				utils.RespondWithMessage(w, http.StatusInternalServerError, "Error checking session.")
				return
			}

			if session.ExpiresAt.Before(time.Now()) {
				utils.RespondWithMessage(w, http.StatusUnauthorized, "Session has expired.")
				return
			}

			// Injection de l'ID utilisateur dans le contexte
			ctx := context.WithValue(r.Context(), UserIDKey, session.UserID)
			next.ServeHTTP(w, r.WithContext(ctx))
		})
	}
}
