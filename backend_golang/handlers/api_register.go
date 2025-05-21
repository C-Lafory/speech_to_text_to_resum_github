// package handlers

// import (
// 	"bytes"
// 	"database/sql"
// 	"encoding/json"
// 	"io"
// 	"log"
// 	"net/http"
// 	"net/mail"

// 	database "api/database/queries"
// 	"api/middleware"
// 	"api/pkg/models"
// 	"api/utils"

// 	"golang.org/x/crypto/bcrypt"
// )

// // HandlerRegister gère l'inscription utilisateur
// func HandlerRegister(db *sql.DB) http.HandlerFunc {
// 	return func(w http.ResponseWriter, r *http.Request) {
// 		utils.SetJSONHeaders(w)

// 		// Gérer les requêtes OPTIONS pour CORS
// 		if r.Method == http.MethodOptions {
// 			w.WriteHeader(http.StatusOK)
// 			return
// 		}

// 		// Vérifier que la méthode est POST
// 		if r.Method != http.MethodPost {
// 			utils.RespondWithMessage(w, http.StatusMethodNotAllowed, "Only POST method is allowed.")
// 			return
// 		}

// 		// Log du corps de la requête pour débogage
// 		body, err := io.ReadAll(r.Body)
// 		if err != nil {
// 			log.Printf("Error reading request body: %v", err)
// 			utils.RespondWithMessage(w, http.StatusBadRequest, "Error reading request body.")
// 			return
// 		}
// 		log.Printf("Received request body: %s", string(body))

// 		// Réinitialiser le corps de la requête pour le décodage
// 		r.Body = io.NopCloser(bytes.NewBuffer(body))

// 		// Décoder le corps de la requête
// 		var user models.UserInfos
// 		if err := json.NewDecoder(r.Body).Decode(&user); err != nil {
// 			log.Printf("JSON decode error: %v", err)
// 			utils.RespondWithMessage(w, http.StatusBadRequest, "Invalid request body.")
// 			return
// 		}

// 		// Validation des champs requis
// 		if user.Username == "" || user.Password == "" || user.Email == "" {
// 			utils.RespondWithMessage(w, http.StatusBadRequest, "All fields (username, password, email) are required.")
// 			return
// 		}

// 		// Validation de l'email
// 		if _, err := mail.ParseAddress(user.Email); err != nil {
// 			utils.RespondWithMessage(w, http.StatusBadRequest, "Invalid email format.")
// 			return
// 		}

// 		// Validation de la complexité du mot de passe
// 		if !utils.IsStrongPassword(user.Password) {
// 			utils.RespondWithMessage(w, http.StatusBadRequest, "Password must be at least 8 characters long and contain a mix of upper/lowercase letters, numbers, and symbols.")
// 			return
// 		}

// 		// Vérification des doublons
// 		exists, err := database.CheckUserExists(db, user.Username, user.Email)
// 		if err != nil {
// 			log.Printf("DB error: %v", err)
// 			utils.RespondWithMessage(w, http.StatusInternalServerError, "Internal server error.")
// 			return
// 		}
// 		if exists {
// 			utils.RespondWithMessage(w, http.StatusConflict, "Username or email already exists.")
// 			return
// 		}

// 		// Hash du mot de passe
// 		hashedPassword, err := bcrypt.GenerateFromPassword([]byte(user.Password), bcrypt.DefaultCost)
// 		if err != nil {
// 			log.Printf("Hashing error: %v", err)
// 			utils.RespondWithMessage(w, http.StatusInternalServerError, "Error hashing password.")
// 			return
// 		}
// 		user.Password = string(hashedPassword)

// 		// Limiteur de tentatives
// 		limiter := middleware.GetClientUsernameLimiter(user.Username)
// 		if !limiter.Allow() {
// 			utils.RespondWithMessage(w, http.StatusTooManyRequests, "Too many attempts for this username. Please try again later.")
// 			return
// 		}

// 		// Insertion en BDD
// 		if err := database.CreateUser(db, &user); err != nil {
// 			log.Printf("DB insertion error: %v", err)
// 			utils.RespondWithMessage(w, http.StatusInternalServerError, "Could not create user.")
// 			return
// 		}

//			// Réponse de succès
//			utils.RespondWithMessage(w, http.StatusCreated, "User created successfully.")
//		}
//	}
package handlers

import (
	"bytes"
	"database/sql"
	"encoding/json"
	"io"
	"log"
	"net/http"
	"net/mail"

	database "api/database/queries"
	"api/middleware"
	"api/pkg/models"
	"api/utils"

	"golang.org/x/crypto/bcrypt"
)

// HandlerRegister gère l'inscription utilisateur
func HandlerRegister(db *sql.DB) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		utils.SetJSONHeaders(w)

		// Gérer les requêtes OPTIONS pour CORS
		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusOK)
			return
		}

		// Vérifier que la méthode est POST
		if r.Method != http.MethodPost {
			log.Println("Requête non autorisée : méthode != POST")
			utils.RespondWithMessage(w, http.StatusMethodNotAllowed, "Only POST method is allowed.")
			return
		}

		// Log du corps de la requête pour débogage
		body, err := io.ReadAll(r.Body)
		if err != nil {
			log.Printf("Erreur lecture du corps de la requête: %v", err)
			utils.RespondWithMessage(w, http.StatusBadRequest, "Error reading request body.")
			return
		}
		log.Printf("Requête d'inscription reçue : %s", string(body))

		// Réinitialiser le corps de la requête pour le décodage
		r.Body = io.NopCloser(bytes.NewBuffer(body))

		// Décoder le corps de la requête
		var user models.UserInfos
		if err := json.NewDecoder(r.Body).Decode(&user); err != nil {
			log.Printf("Erreur décodage JSON: %v", err)
			utils.RespondWithMessage(w, http.StatusBadRequest, "Invalid request body.")
			return
		}

		log.Printf("Début inscription pour utilisateur: %s / email: %s", user.Username, user.Email)

		// Validation des champs requis
		if user.Username == "" || user.Password == "" || user.Email == "" {
			log.Println("Champs requis manquants")
			utils.RespondWithMessage(w, http.StatusBadRequest, "All fields (username, password, email) are required.")
			return
		}

		// Validation de l'email
		if _, err := mail.ParseAddress(user.Email); err != nil {
			log.Printf("Email invalide: %s", user.Email)
			utils.RespondWithMessage(w, http.StatusBadRequest, "Invalid email format.")
			return
		}

		// Validation de la complexité du mot de passe
		if !utils.IsStrongPassword(user.Password) {
			log.Printf("Mot de passe trop faible pour l'utilisateur: %s", user.Username)
			utils.RespondWithMessage(w, http.StatusBadRequest, "Password must be at least 8 characters long and contain a mix of upper/lowercase letters, numbers, and symbols.")
			return
		}

		// Vérification des doublons
		exists, err := database.CheckUserExists(db, user.Username, user.Email)
		if err != nil {
			log.Printf("Erreur DB lors de la vérification d'existence: %v", err)
			utils.RespondWithMessage(w, http.StatusInternalServerError, "Internal server error.")
			return
		}
		if exists {
			log.Printf("Échec inscription : utilisateur ou email déjà existant (%s / %s)", user.Username, user.Email)
			utils.RespondWithMessage(w, http.StatusConflict, "Username or email already exists.")
			return
		}

		// Hash du mot de passe
		hashedPassword, err := bcrypt.GenerateFromPassword([]byte(user.Password), bcrypt.DefaultCost)
		if err != nil {
			log.Printf("Erreur lors du hash du mot de passe: %v", err)
			utils.RespondWithMessage(w, http.StatusInternalServerError, "Error hashing password.")
			return
		}
		user.Password = string(hashedPassword)

		// Limiteur de tentatives
		limiter := middleware.GetClientUsernameLimiter(user.Username)
		if !limiter.Allow() {
			log.Printf("Trop de tentatives d'inscription pour l'utilisateur: %s", user.Username)
			utils.RespondWithMessage(w, http.StatusTooManyRequests, "Too many attempts for this username. Please try again later.")
			return
		}

		// Insertion en BDD
		if err := database.CreateUser(db, &user); err != nil {
			log.Printf("Erreur DB lors de la création d'utilisateur: %v", err)
			utils.RespondWithMessage(w, http.StatusInternalServerError, "Could not create user.")
			return
		}

		log.Printf("Inscription réussie pour l'utilisateur: %s", user.Username)

		utils.RespondWithMessage(w, http.StatusCreated, "User created successfully.")
	}
}
