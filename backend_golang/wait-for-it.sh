#!/bin/sh

HOSTPORT="$1"
TIMEOUT="$2"

# Vérification des arguments
if [ -z "$HOSTPORT" ] || [ -z "$TIMEOUT" ]; then
  echo "Usage: $0 host:port timeout_in_seconds -- command_to_run"
  exit 1
fi

# Extraire hôte et port
HOST=$(echo "$HOSTPORT" | cut -d: -f1)
PORT=$(echo "$HOSTPORT" | cut -d: -f2)

echo "⏳ Attente de $HOST:$PORT pendant $TIMEOUT secondes..."

# Calcul du temps d'attente
START_TIME=$(date +%s)

while true; do
  nc -z "$HOST" "$PORT" >/dev/null 2>&1
  if [ $? -eq 0 ]; then
    echo "✅ $HOST:$PORT est disponible."
    shift 3  # ignorer host:port, timeout, et "--"
    exec "$@"
    exit 0
  fi

  CURRENT_TIME=$(date +%s)
  ELAPSED=$((CURRENT_TIME - START_TIME))

  if [ "$ELAPSED" -ge "$TIMEOUT" ]; then
    echo "❌ Timeout après $TIMEOUT secondes en attendant $HOST:$PORT"
    exit 1
  fi

  sleep 1
done
