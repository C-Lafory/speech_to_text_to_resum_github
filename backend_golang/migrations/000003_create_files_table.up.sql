CREATE TABLE IF NOT EXISTS files (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Identifiant unique pour chaque fichier.
    user_id INT NOT NULL,              -- Référence à l'utilisateur.
    audio_input VARCHAR(255) NOT NULL, -- Chemin du fichier audio d'entrée.
    transcription_path VARCHAR(255),   -- Chemin du fichier de transcription.
    summary_path VARCHAR(255),         -- Chemin du fichier de résumé.
    audio_output_path VARCHAR(255),    -- Chemin du fichier audio de sortie.
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- Date de création.
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE -- Clé étrangère vers la table users.
); 