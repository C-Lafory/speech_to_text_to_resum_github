#!/bin/sh

echo "⏳ Attente de MySQL (mysql:3306)..."
/wait-for-it.sh mysql:3306 30 -- echo "✅ MySQL est prêt"

echo "🚀 Lancement de l'API Go..."
exec /app/main
