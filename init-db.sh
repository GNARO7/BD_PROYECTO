#!/bin/bash
set -e

# Esperar a que PostgreSQL esté listo
until pg_isready -h localhost -p 5432 -U "$POSTGRES_USER"; do
  echo "Esperando a que PostgreSQL esté listo..."
  sleep 2
done

# Crear la base de datos si no existe
psql -U "$POSTGRES_USER" -tc "SELECT 1 FROM pg_database WHERE datname = '$POSTGRES_DB'" | grep -q 1 || psql -U "$POSTGRES_USER" -c "CREATE DATABASE $POSTGRES_DB"

# Restaurar el dump en la base de datos especificada usando pg_restore
pg_restore -U "$POSTGRES_USER" -d "$POSTGRES_DB" /dump/backup.dump
