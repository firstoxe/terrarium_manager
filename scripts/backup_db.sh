#!/usr/bin/env bash
set -euo pipefail
mkdir -p backups
STAMP=$(date +%Y%m%d_%H%M%S)
OUT="backups/terrarium_${STAMP}.sql"
PGPASSWORD="${DB_PASSWORD:-${DB_PASS:-}}" pg_dump \
  --host="${DB_HOST:-localhost}" \
  --port="${DB_PORT:-5432}" \
  --username="${DB_USER:-postgres}" \
  --dbname="${DB_NAME:-terrarium_manager}" \
  --file="$OUT"
echo "Wrote $OUT"
