CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Identifiant unique pour chaque utilisateur.
    username VARCHAR(50) NOT NULL UNIQUE,     -- Nom d'utilisateur (obligatoire).
    password VARCHAR(256) NOT NULL,    -- Mot de passe (obligatoire, haché).
    email VARCHAR(100) NOT NULL UNIQUE -- Email (obligatoire, doit être unique).
    
);