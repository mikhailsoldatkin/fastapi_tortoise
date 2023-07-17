#!/bin/sh
# wait-for-it.sh: Ожидание доступности указанного хоста:порта или истечения таймаута
export $(cat .env | xargs)

host="$DB_HOST"
port="$DB_PORT"
timeout=5

echo "Ожидание доступности $host:$port..."

while ! nc -z "$host" "$port"; do
  timeout=$((timeout - 1))
  if [ "$timeout" -eq 0 ]; then
    echo "Истекло время ожидания. $host:$port недоступен."
    exit 1
  fi
  sleep 1
done

echo "$host:$port доступен!"
exit 0
