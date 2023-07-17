#!/bin/sh
# wait-for-it.sh: Wait until a given host:port is available or timeout

host="db"
port="5432"
timeout="${10:-15}"

echo "Waiting for $host:$port to be available..."

while ! nc -z "$host" "$port"; do
  timeout=$((timeout - 1))
  if [ "$timeout" -eq 0 ]; then
    echo "Timeout reached. $host:$port is not available."
    exit 1
  fi
  sleep 1
done

echo "$host:$port is available!"
exit 0

