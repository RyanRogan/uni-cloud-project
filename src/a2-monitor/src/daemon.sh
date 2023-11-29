#!/bin/bash

set -e

exec python3 /app/monitor.py &
exec python3 /app/app.py 