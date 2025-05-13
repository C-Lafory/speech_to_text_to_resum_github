package handlers

import (
	"database/sql"
	"net/http"

	database "api/database/queries"
	"api/middleware"
	"api/utils"
)

func HandlerGetUserFiles(db *sql.DB) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		utils.SetJSONHeaders(w)

		// 🔐 Authentification via middleware
		userID, ok := r.Context().Value(middleware.UserIDKey).(int)
		if !ok || userID == 0 {
			utils.RespondWithMessage(w, http.StatusUnauthorized, "Unauthorized")
			return
		}

		// 🔍 Récupération en BDD
		files, err := database.GetFilesByUserID(db, userID)
		if err != nil {
			utils.RespondWithMessage(w, http.StatusInternalServerError, "Error fetching files")
			return
		}

		// ✅ Réponse
		utils.RespondWithJSON(w, http.StatusOK, files)
	}
}
