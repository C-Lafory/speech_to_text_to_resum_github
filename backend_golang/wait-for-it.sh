#!/bin/sh

HOSTPORT="$1"
TIMEOUT="${3:-15}"

HOST=$(echo "$HOSTPORT" | cut -d: -f1)
PORT=$(echo "$HOSTPORT" | cut -d: -f2)

echo "⏳ Attente de $HOST:$PORT pendant $TIMEOUT secondes..."

end=$((SECONDS+TIMEOUT))

while [ $SECONDS -lt $end ]; do
    nc -z "$HOST" "$PORT" >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "✅ $HOST:$PORT est disponible."
        shift 4 # pour ignorer --strict -- et l'host:port
        exec "$@"
        exit 0
    fi
    sleep 1
done

echo "❌ Timeout après $TIMEOUT secondes en attendant $HOST:$PORT"
exit 1
