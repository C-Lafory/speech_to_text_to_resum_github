package models

type UserInfos struct {
    ID       int    `json:"id"`       // Identifiant unique de l'utilisateur.
    Username string `json:"username"` // Nom d'utilisateur.
    Password string `json:"password"` // Mot de passe haché.
    Email    string `json:"email"`    // Adresse email unique.
}

