package middleware

import (
	"api/database/queries"
	"api/utils"
	"context"
	"database/sql"
	"errors"
	"net/http"
	"strings"
	"time"

	"golang.org/x/crypto/bcrypt"
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

			session, err := database.GetSessionByToken(db, tokenRaw)
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

			if err := bcrypt.CompareHashAndPassword([]byte(session.Token), []byte(tokenRaw)); err != nil {
				utils.RespondWithMessage(w, http.StatusUnauthorized, "Invalid session token.")
				return
			}

			// Injection de l'ID utilisateur dans le contexte
			ctx := context.WithValue(r.Context(), UserIDKey, session.UserID)
			next.ServeHTTP(w, r.WithContext(ctx))
		})
	}
}
