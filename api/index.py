# ═══════════════════════════════════════════════════════
# POINT D'ENTRÉE VERCEL SERVERLESS
# ═══════════════════════════════════════════════════════

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from datetime import datetime
import os

# Importer depuis le même dossier (api/)
from utils.ai_handler import generate_summary
from utils.pdf_generator import create_pdf

# ═══════════════════════════════════════════════════════
# INITIALISATION FLASK
# ═══════════════════════════════════════════════════════

app = Flask(__name__)

# Configuration CORS
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# ═══════════════════════════════════════════════════════
# ROUTES
# ═══════════════════════════════════════════════════════

@app.route('/api/health', methods=['GET'])
def health_check():
    """Vérification que l'API fonctionne"""
    return jsonify({
        "status": "online",
        "message": "SyntheSIA API is running on Vercel!",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/generate-report', methods=['POST', 'OPTIONS'])
def generate_report():
    """Génère un rapport PDF"""
    
    # Gérer preflight CORS
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        # Récupération des données
        data = request.json
        title = data.get('title', 'Rapport sans titre')
        raw_data = data.get('raw_data', '')
        author = data.get('author', 'Anonyme')
        role = data.get('role', 'Non spécifié')
        
        if not raw_data:
            return jsonify({"error": "Aucune donnée fournie"}), 400
        
        # Génération IA
        print(f"🤖 Génération du résumé IA pour : {title}")
        summary = generate_summary(raw_data)
        
        # Création PDF
        print(f"📄 Création du PDF...")
        pdf_path = create_pdf(title, summary, author, role)
        
        # Envoi du PDF
        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"rapport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
        
    except Exception as e:
        print(f"❌ Erreur : {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# ═══════════════════════════════════════════════════════
# EXPORT POUR VERCEL
# ═══════════════════════════════════════════════════════

# Vercel détecte automatiquement cette variable
handler = app