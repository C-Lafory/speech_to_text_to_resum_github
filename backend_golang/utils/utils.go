package utils

import (
	"encoding/json"
	"net/http"
	"regexp"
)

// Envoie une réponse JSON standardisée
func RespondWithJSON(w http.ResponseWriter, status int, payload interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(payload)
} // voir si mettre un champs success est utile ou non

// Définit les headers communs (ex. pour CORS et JSON)
func SetJSONHeaders(w http.ResponseWriter) {
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Access-Control-Allow-Origin", "*") // À restreindre en prod
}

// Vérifie la complexité d’un mot de passe
func IsStrongPassword(password string) bool {
	// Min 8 caractères, au moins une majuscule, une minuscule, un chiffre et un caractère spécial
	passwordRegex := regexp.MustCompile(`^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z0-9]).{8,}$`)
	return passwordRegex.MatchString(password)
}

// Envoie une réponse de succès simple : {"message": "..."}
func RespondWithMessage(w http.ResponseWriter, status int, message string) {
	RespondWithJSON(w, status, map[string]string{
		"message": message,
	})
}