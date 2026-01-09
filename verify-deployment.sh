#!/bin/bash
# Script de vérification pré-déploiement SyntheSIA

echo "═══════════════════════════════════════════════════════"
echo "🔍 VÉRIFICATION PRÉ-DÉPLOIEMENT SYNTHESIA"
echo "═══════════════════════════════════════════════════════"
echo ""

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0

# 1. Vérifier les fichiers requis
echo "📁 Vérification des fichiers..."
FILES=(
    "api/health.py"
    "api/generate-report.py"
    "api/utils/ai_handler.py"
    "api/utils/pdf_generator.py"
    "vercel.json"
    "requirements.txt"
    "frontend/index.html"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✅${NC} $file"
    else
        echo -e "${RED}❌${NC} $file (MANQUANT)"
        ((ERRORS++))
    fi
done

echo ""

# 2. Vérifier les imports Python
echo "🐍 Vérification des imports Python..."
python3 -c "
import sys
import os

# Ajouter api au path
sys.path.insert(0, 'api')

try:
    from utils.ai_handler import generate_summary
    print('✅ utils.ai_handler OK')
except Exception as e:
    print(f'❌ utils.ai_handler: {e}')
    sys.exit(1)

try:
    from utils.pdf_generator import create_pdf
    print('✅ utils.pdf_generator OK')
except Exception as e:
    print(f'❌ utils.pdf_generator: {e}')
    sys.exit(1)
" 2>&1

if [ $? -ne 0 ]; then
    ((ERRORS++))
fi

echo ""

# 3. Vérifier vercel.json
echo "⚙️  Vérification vercel.json..."
if python3 -c "import json; json.load(open('vercel.json'))" 2>/dev/null; then
    echo -e "${GREEN}✅${NC} vercel.json est valide"
else
    echo -e "${RED}❌${NC} vercel.json est invalide"
    ((ERRORS++))
fi

# 4. Vérifier requirements.txt
echo "📦 Vérification requirements.txt..."
if [ -f "requirements.txt" ] && [ -s "requirements.txt" ]; then
    echo -e "${GREEN}✅${NC} requirements.txt existe et n'est pas vide"
    echo "   Dépendances:"
    grep -v "^#" requirements.txt | grep -v "^$" | sed 's/^/   - /'
else
    echo -e "${RED}❌${NC} requirements.txt manquant ou vide"
    ((ERRORS++))
fi

echo ""

# 5. Vérifier que GROQ_API_KEY n'est pas dans le code
echo "🔒 Vérification sécurité (pas de clés API dans le code)..."
if grep -r "GROQ_API_KEY.*=.*['\"]" api/ 2>/dev/null; then
    echo -e "${RED}❌${NC} Clé API trouvée dans le code !"
    ((ERRORS++))
else
    echo -e "${GREEN}✅${NC} Aucune clé API hardcodée"
fi

# 6. Vérifier l'utilisation de /tmp dans pdf_generator
echo "📄 Vérification utilisation /tmp dans pdf_generator..."
if grep -q "/tmp\|tempfile" api/utils/pdf_generator.py; then
    echo -e "${GREEN}✅${NC} pdf_generator utilise /tmp"
else
    echo -e "${YELLOW}⚠️${NC}  pdf_generator pourrait ne pas utiliser /tmp"
fi

echo ""

# 7. Résumé
echo "═══════════════════════════════════════════════════════"
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ TOUTES LES VÉRIFICATIONS RÉUSSIES${NC}"
    echo ""
    echo "🚀 Prêt pour le déploiement !"
    echo ""
    echo "Prochaines étapes:"
    echo "1. Vérifier que GROQ_API_KEY est définie dans Vercel Dashboard"
    echo "2. git add ."
    echo "3. git commit -m 'Migration vers handlers Vercel natifs'"
    echo "4. git push origin main"
    echo "5. Vérifier les logs dans Vercel Dashboard"
    exit 0
else
    echo -e "${RED}❌ $ERRORS ERREUR(S) TROUVÉE(S)${NC}"
    echo ""
    echo "⚠️  Corrigez les erreurs avant de déployer"
    exit 1
fi

