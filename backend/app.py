from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from utils.ai_handler import generate_summary
from utils.pdf_generator import create_pdf
import os
from datetime import datetime

# Initialisation de l'application Flask
app = Flask(__name__)

# ═══════════════════════════════════════════════════════
# CONFIGURATION CORS (TRÈS IMPORTANT POUR VERCEL)
# ═══════════════════════════════════════════════════════
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Route de test
@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple vérification que l'API est en ligne"""
    return jsonify({
        "status": "online",
        "message": "SyntheSIA API is running!"
    })

# Route principale
@app.route('/api/generate-report', methods=['POST', 'OPTIONS'])
def generate_report():
    """
    Génère un rapport PDF à partir de données textuelles
    """
    # Gérer les requêtes OPTIONS (preflight CORS)
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
        return jsonify({"error": str(e)}), 500

# ═══════════════════════════════════════════════════════
# CONFIGURATION POUR VERCEL (SERVERLESS)
# ═══════════════════════════════════════════════════════

# Cette variable est nécessaire pour Vercel
app = app

# Handler pour les fonctions serverless Vercel
def handler(request, context):
    """Point d'entrée pour Vercel Serverless Functions"""
    return app(request.environ, context)

# Pour développement local uniquement
if __name__ == '__main__':
    app.run(debug=True, port=5000)