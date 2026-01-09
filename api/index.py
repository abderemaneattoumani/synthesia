from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from datetime import datetime
import os
import sys

# Ajouter le dossier api au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Imports des utilitaires
from utils.ai_handler import generate_summary
from utils.pdf_generator import create_pdf

# ═══════════════════════════════════════════════════════
# INITIALISATION FLASK
# ═══════════════════════════════════════════════════════

app = Flask(__name__)

# Configuration CORS simple
CORS(app)

# ═══════════════════════════════════════════════════════
# ROUTES
# ═══════════════════════════════════════════════════════

@app.route('/api/health', methods=['GET'])
def health():
    """Vérification santé de l'API"""
    return jsonify({
        "status": "online",
        "message": "SyntheSIA API is running!",
        "timestamp": datetime.now().isoformat(),
        "groq_configured": bool(os.environ.get('GROQ_API_KEY'))
    })

@app.route('/api/generate-report', methods=['POST', 'OPTIONS'])
def generate_report():
    """Génération de rapport PDF"""
    
    # Gérer preflight CORS
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response, 204
    
    try:
        # Récupération des données
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Aucune donnée JSON reçue"}), 400
        
        title = data.get('title', 'Rapport sans titre')
        raw_data = data.get('raw_data', '')
        author = data.get('author', 'Anonyme')
        role = data.get('role', 'Non spécifié')
        
        if not raw_data:
            return jsonify({"error": "Le champ raw_data est requis"}), 400
        
        # Génération IA
        summary = generate_summary(raw_data)
        
        # Création PDF
        pdf_path = create_pdf(title, summary, author, role)
        
        # Envoi du fichier
        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"rapport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
        
    except Exception as e:
        import traceback
        print(f"Erreur: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

# ═══════════════════════════════════════════════════════
# POINT D'ENTRÉE VERCEL (CRITIQUE)
# ═══════════════════════════════════════════════════════

# Pour Vercel Serverless Functions
app = app