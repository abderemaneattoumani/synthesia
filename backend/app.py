from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from utils.ai_handler import generate_summary
from utils.pdf_generator import create_pdf
import os
from datetime import datetime

# Initialisation de l'application Flask
app = Flask(__name__)
CORS(app)  # Permet les requêtes depuis le frontend

# Route de test (vérifie que le serveur fonctionne)
@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple vérification que l'API est en ligne"""
    return jsonify({
        "status": "online",
        "message": "SyntheSIA API is running!"
    })

# Route principale : génération de rapport
@app.route('/api/generate-report', methods=['POST'])
def generate_report():
    """
    Reçoit des données, appelle l'IA, génère un PDF
    
    Données attendues (JSON) :
    {
        "title": "Titre du rapport",
        "raw_data": "Notes techniques brutes...",
        "author": "Nom de l'auteur",
        "role": "Poste de l'auteur"
    }
    """
    try:
        # Récupération des données envoyées par le frontend
        data = request.json
        title = data.get('title', 'Rapport sans titre')
        raw_data = data.get('raw_data', '')
        author = data.get('author', 'Anonyme')
        role = data.get('role', 'Non spécifié')  # ← NOUVEAU
        
        # Vérification que les données ne sont pas vides
        if not raw_data:
            return jsonify({"error": "Aucune donnée fournie"}), 400
        
        # ÉTAPE 1 : Appel à l'IA pour générer le résumé
        print(f"🤖 Génération du résumé IA pour : {title}")
        summary = generate_summary(raw_data)
        
        # ÉTAPE 2 : Création du PDF avec le résumé
        print(f"📄 Création du PDF...")
        pdf_path = create_pdf(title, summary, author, role)  # ← MODIFIÉ
        
        # ÉTAPE 3 : Envoi du PDF au frontend
        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"rapport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
        
    except Exception as e:
        print(f"❌ Erreur : {str(e)}")
        return jsonify({"error": str(e)}), 500

# Lancement du serveur
if __name__ == '__main__':
    app.run(debug=True, port=5000)

# Pour Vercel (serverless)
app = app