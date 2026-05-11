#!/usr/bin/env bash
# cleanup_fase0.sh
# Ejecutar desde la raíz del proyecto: bash cleanup_fase0.sh

set -e
ROOT="$(pwd)"
BACKEND="$ROOT/backend"

echo "── Fase 0: Limpieza del proyecto ERP ──"

# 1. Eliminar generated.py (clases duplicadas)
GENERATED="$BACKEND/app/models/generated.py"
if [ -f "$GENERATED" ]; then
    rm "$GENERATED"
    echo "✅ Eliminado: app/models/generated.py"
else
    echo "⏭  No existe: app/models/generated.py"
fi

# 2. Eliminar repositorio duplicado fuera de app/
REPO_DUPLICADO="$BACKEND/repositories"
if [ -d "$REPO_DUPLICADO" ]; then
    rm -rf "$REPO_DUPLICADO"
    echo "✅ Eliminado: backend/repositories/ (duplicado)"
else
    echo "⏭  No existe: backend/repositories/"
fi

# 3. Reemplazar migrations/env.py con la versión corregida
echo ""
echo "── Archivos que debes reemplazar manualmente ──"
echo ""
echo "  1. backend/migrations/env.py"
echo "     → Reemplaza con el archivo env.py entregado"
echo ""
echo "  2. backend/alembic.ini"
echo "     → Reemplaza con el alembic.ini entregado"
echo ""
echo "  3. Copia .env.example a la raíz de backend/"
echo "     → cp .env.example backend/.env.example"
echo "     → cp backend/.env.example backend/.env"
echo "     → Edita backend/.env con tus valores reales"
echo ""
echo "── Verifica que .env NO esté en git ──"
if grep -q "^\.env$" "$ROOT/.gitignore" 2>/dev/null; then
    echo "✅ .env está en .gitignore"
else
    echo "⚠️  Agrega .env a tu .gitignore raíz"
fi

echo ""
echo "✅ Fase 0 completada"