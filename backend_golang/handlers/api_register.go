package handlers

import (
    "database/sql"
    "encoding/json"
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

        // Vérifier que la méthode est POST
        if r.Method != http.MethodPost {
            utils.RespondWithMessage(w, http.StatusMethodNotAllowed, "Only POST method is allowed.")
            return
        }

        // Décoder le corps de la requête
        var user models.UserInfos
        if err := json.NewDecoder(r.Body).Decode(&user); err != nil {
            utils.RespondWithMessage(w, http.StatusBadRequest, "Invalid request body.")
            return
        }

        // Validation des champs requis
        if user.Username == "" || user.Password == "" || user.Email == "" {
            utils.RespondWithMessage(w, http.StatusBadRequest, "All fields (username, password, email) are required.")
            return
        }

        // Validation de l'email
        if _, err := mail.ParseAddress(user.Email); err != nil {
            utils.RespondWithMessage(w, http.StatusBadRequest, "Invalid email format.")
            return
        }

        // Validation de la complexité du mot de passe
        if !utils.IsStrongPassword(user.Password) {
            utils.RespondWithMessage(w, http.StatusBadRequest, "Password must be at least 8 characters long and contain a mix of upper/lowercase letters, numbers, and symbols.")
            return
        }

        // Vérification des doublons
        exists, err := database.CheckUserExists(db, user.Username, user.Email)
        if err != nil {
            log.Printf("DB error: %v", err)
            utils.RespondWithMessage(w, http.StatusInternalServerError, "Internal server error.")
            return
        }
        if exists {
            utils.RespondWithMessage(w, http.StatusConflict, "Username or email already exists.")
            return
        }

        // Hash du mot de passe
        hashedPassword, err := bcrypt.GenerateFromPassword([]byte(user.Password), bcrypt.DefaultCost)
        if err != nil {
			log.Printf("Hashing error: %v", err)
            utils.RespondWithMessage(w, http.StatusInternalServerError, "Error hashing password.")
            return
        }
        user.Password = string(hashedPassword)

        // Limiteur de tentatives
        limiter := middleware.GetClientUsernameLimiter(user.Username)
        if !limiter.Allow() {
            utils.RespondWithMessage(w, http.StatusTooManyRequests, "Too many attempts for this username. Please try again later.")
            return
        }

        // Insertion en BDD
        if err := database.CreateUser(db, &user); err != nil {
            log.Printf("DB insertion error: %v", err)
            utils.RespondWithMessage(w, http.StatusInternalServerError, "Could not create user.")
            return
        }

        // Réponse de succès
        utils.RespondWithMessage(w, http.StatusCreated, "User created successfully.")
    }
}