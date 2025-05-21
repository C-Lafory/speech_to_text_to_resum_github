package handlers

import (
	"database/sql"
	"encoding/json"
	"log"
	"net/http"
	"time"

	database "api/database/queries"
	"api/middleware"
	"api/utils"

	"golang.org/x/crypto/bcrypt"
)

// Durée de vie d’une session (par ex. 7 jours)
const sessionDuration = 7 * 24 * time.Hour

// func HandlerLogin(db *sql.DB) http.HandlerFunc {
// 	return func(w http.ResponseWriter, r *http.Request) {

//         // Supprimer les anciennes sessions expirées
//         _ = database.DeleteExpiredSessions(db) // on ignore l'erreur pour ne pas bloquer le login

// 		utils.SetJSONHeaders(w)

// 		if r.Method != http.MethodPost {
// 			utils.RespondWithMessage(w, http.StatusMethodNotAllowed, "Only POST method is allowed.")
// 			return
// 		}

// 		// Decode body
// 		var creds struct {
// 			Username string `json:"username"`
// 			Password string `json:"password"`
// 		}
// 		if err := json.NewDecoder(r.Body).Decode(&creds); err != nil {
// 			utils.RespondWithMessage(w, http.StatusBadRequest, "Invalid request body.")
// 			return
// 		}

// 		limiter := middleware.GetClientUsernameLimiter(creds.Username)
// 		if !limiter.Allow() {
// 			utils.RespondWithMessage(w, http.StatusTooManyRequests, "Too many login attempts. Please wait before trying again.")
// 			return
// 		}

// 		// Récupérer l'utilisateur
// 		user, err := database.GetUserByUsername(db, creds.Username)
// 		if err != nil {
// 			utils.RespondWithMessage(w, http.StatusUnauthorized, "Invalid username or password.")
// 			return
// 		}

// 		// Vérifier le mot de passe
// 		if err := bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(creds.Password)); err != nil {
// 			utils.RespondWithMessage(w, http.StatusUnauthorized, "Invalid username or password.")
// 			return
// 		}

// 		rawToken, err := utils.GenerateSecureToken(32) // 256 bits
// 		if err != nil {
// 			utils.RespondWithMessage(w, http.StatusInternalServerError, "Error generating secure token.")
// 			return
// 		}

//         hashedToken := utils.HashToken(rawToken)

// 		// Expiration
// 		expiresAt := time.Now().Add(sessionDuration)

// 		// Enregistrer la session en BDD
// 		err = database.CreateSession(db, user.ID, string(hashedToken), expiresAt)
// 		if err != nil {
// 			utils.RespondWithMessage(w, http.StatusInternalServerError, "Error creating session.")
// 			return
// 		}

// 		// Répondre au client avec le token BRUT
// 		utils.RespondWithJSON(w, http.StatusOK, map[string]interface{}{
// 			"message": "Login successful.",
// 			"token":   rawToken, // attention, ce token ne doit pas être loggué côté serveur
// 		})
// 	}
// }

func HandlerLogin(db *sql.DB) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		_ = database.DeleteExpiredSessions(db) // nettoyage des sessions expirées

		utils.SetJSONHeaders(w)

		if r.Method != http.MethodPost {
			utils.RespondWithMessage(w, http.StatusMethodNotAllowed, "Only POST method is allowed.")
			return
		}

		// Decode body
		var creds struct {
			Username string `json:"username"`
			Password string `json:"password"`
		}
		if err := json.NewDecoder(r.Body).Decode(&creds); err != nil {
			log.Println("Erreur lors du décodage JSON du login:", err)
			utils.RespondWithMessage(w, http.StatusBadRequest, "Invalid request body.")
			return
		}

		log.Printf("Tentative de connexion pour l'utilisateur: %s", creds.Username)

		limiter := middleware.GetClientUsernameLimiter(creds.Username)
		if !limiter.Allow() {
			log.Printf("Trop de tentatives de connexion pour l'utilisateur: %s", creds.Username)
			utils.RespondWithMessage(w, http.StatusTooManyRequests, "Too many login attempts. Please wait before trying again.")
			return
		}

		user, err := database.GetUserByUsername(db, creds.Username)
		if err != nil {
			log.Printf("Utilisateur introuvable ou erreur DB pour: %s", creds.Username)
			utils.RespondWithMessage(w, http.StatusUnauthorized, "Invalid username or password.")
			return
		}

		if err := bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(creds.Password)); err != nil {
			log.Printf("Mot de passe invalide pour l'utilisateur: %s", creds.Username)
			utils.RespondWithMessage(w, http.StatusUnauthorized, "Invalid username or password.")
			return
		}

		rawToken, err := utils.GenerateSecureToken(32)
		if err != nil {
			log.Println("Erreur lors de la génération du token sécurisé:", err)
			utils.RespondWithMessage(w, http.StatusInternalServerError, "Error generating secure token.")
			return
		}

		hashedToken := utils.HashToken(rawToken)
		expiresAt := time.Now().Add(sessionDuration)

		err = database.CreateSession(db, user.ID, string(hashedToken), expiresAt)
		if err != nil {
			log.Printf("Erreur lors de la création de session pour l'utilisateur %s: %v", creds.Username, err)
			utils.RespondWithMessage(w, http.StatusInternalServerError, "Error creating session.")
			return
		}

		log.Printf("Connexion réussie pour l'utilisateur: %s", creds.Username)

		utils.RespondWithJSON(w, http.StatusOK, map[string]interface{}{
			"message": "Login successful.",
			"token":   rawToken, // ne jamais logger ce token
		})
	}
}
