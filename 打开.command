#!/bin/bash
# Serve the package over http so ES module imports resolve; file:// would be
# blocked by the browser's module CORS rules and most pages would stay blank.
cd "$(dirname "$0")" || exit 1
PORT=8123
while lsof -nP -iTCP:$PORT -sTCP:LISTEN >/dev/null 2>&1; do PORT=$((PORT+1)); done
echo "Serving on http://127.0.0.1:$PORT  (close this window to stop)"
python3 -m http.server "$PORT" >/dev/null 2>&1 &
SERVER=$!
trap 'kill $SERVER 2>/dev/null' EXIT INT TERM
sleep 1
open "http://127.0.0.1:$PORT/index.html"
wait $SERVER
