#!/bin/sh

HOSTPORT="$1"
shift

# Valeur par défaut du timeout
TIMEOUT=15

# Lecture des arguments supplémentaires
while [ $# -gt 0 ]; do
  case "$1" in
    --timeout=*)
      TIMEOUT="${1#*=}"
      ;;
    --timeout)
      shift
      TIMEOUT="$1"
      ;;
    --)
      shift
      break
      ;;
  esac
  shift
done

HOST=$(echo "$HOSTPORT" | cut -d: -f1)
PORT=$(echo "$HOSTPORT" | cut -d: -f2)

echo "⏳ Attente de $HOST:$PORT pendant $TIMEOUT secondes..."

end=$((SECONDS+TIMEOUT))

while [ $SECONDS -lt $end ]; do
  nc -z "$HOST" "$PORT" >/dev/null 2>&1
  if [ $? -eq 0 ]; then
    echo "✅ $HOST:$PORT est disponible."
    exec "$@"
    exit 0
  fi
  sleep 1
done

echo "❌ Timeout après $TIMEOUT secondes en attendant $HOST:$PORT"
exit 1
