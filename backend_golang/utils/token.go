package utils

import (
	"crypto/rand"
	"crypto/sha256"
	"encoding/hex"
)

func HashToken(token string) string {
	hash := sha256.Sum256([]byte(token))
	return hex.EncodeToString(hash[:])
}

// Génère un token sécurisé avec N octets aléatoires (ex : 32 pour 256 bits)
func GenerateSecureToken(nBytes int) (string, error) {
	b := make([]byte, nBytes)
	_, err := rand.Read(b)
	if err != nil {
		return "", err
	}
	return hex.EncodeToString(b), nil // ex : 64 caractères hex
}
