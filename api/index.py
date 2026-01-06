# ═══════════════════════════════════════════════════════
# POINT D'ENTRÉE VERCEL SERVERLESS
# ═══════════════════════════════════════════════════════

import sys
import os

# Ajouter le dossier backend au path Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Importer l'application Flask depuis backend/app.py
from app import app

# Vercel va automatiquement détecter cette variable
# C'est le point d'entrée de la fonction serverless
handler = app