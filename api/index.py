"""
point d'entrée principal pour vercel
application flask complète et optimisée
"""
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import sys
import traceback

# configuration du chemin pour les imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# créer l'application flask
app = Flask(__name__)

# configuration cors pour permettre les requêtes depuis le frontend
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# logs au démarrage
print("=" * 60)
print("SYNTHESIA API - DEMARRAGE")
print("=" * 60)
print(f"python version: {sys.version}")
print(f"working directory: {os.getcwd()}")
print(f"api directory: {current_dir}")
print(f"groq_api_key configured: {bool(os.environ.get('GROQ_API_KEY'))}")
print("=" * 60)

@app.route('/api/health', methods=['GET', 'OPTIONS'])
def health():
    """
    route de vérification de santé
    retourne le statut de l'api et la configuration
    """
    try:
        print("route /api/health appelee")
        
        # vérifier la configuration
        groq_configured = bool(os.environ.get('GROQ_API_KEY'))
        
        # réponse json
        response = {
            "status": "online",
            "message": "SyntheSIA API is running",
            "groq_configured": groq_configured,
            "environment": "production" if os.environ.get('VERCEL') else "development"
        }
        
        print(f"reponse health: {response}")
        return jsonify(response)
        
    except Exception as e:
        print(f"erreur dans health: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500

@app.route('/api/generate-report', methods=['POST', 'OPTIONS'])
def generate_report():
    """
    route principale pour générer un rapport pdf
    accepte les données du formulaire et retourne un pdf
    """
    try:
        print("route /api/generate-report appelee")
        
        # gestion des requêtes options (cors preflight)
        if request.method == 'OPTIONS':
            print("requete options (cors)")
            return '', 204
        
        # parser les données json de la requête
        data = request.get_json()
        
        if not data:
            print("aucune donnee recue")
            return jsonify({"error": "No data provided"}), 400
        
        # validation des données requises
        if not data.get('raw_data'):
            print("raw_data manquant")
            return jsonify({"error": "Missing raw_data field"}), 400
        
        # extraire les données du formulaire
        title = data.get('title', 'Rapport')
        raw_data = data.get('raw_data', '')
        author = data.get('author', 'Anonyme')
        role = data.get('role', 'Technicien')
        
        print(f"titre: {title}")
        print(f"auteur: {author}")
        print(f"role: {role}")
        print(f"donnees brutes: {len(raw_data)} caracteres")
        
        # importer les utilitaires (imports locaux pour éviter les erreurs)
        print("import des utilitaires...")
        from utils.ai_handler import generate_summary
        from utils.pdf_generator import create_pdf
        print("utilitaires importes")
        
        # étape 1: générer le résumé avec l'ia groq
        print("etape 1: generation du resume ia...")
        summary = generate_summary(raw_data)
        print(f"resume genere ({len(summary)} caracteres)")
        
        # étape 2: générer le pdf avec le résumé
        print("etape 2: generation du pdf...")
        pdf_path = create_pdf(title, summary, author, role)
        print(f"pdf cree: {pdf_path}")
        
        # étape 3: retourner le pdf au client
        print("etape 3: envoi du pdf...")
        
        # utiliser send_file de flask pour envoyer le pdf
        response = send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'rapport_{title.replace(" ", "_")}.pdf'
        )
        
        print("pdf envoye avec succes")
        return response
        
    except Exception as e:
        # gestion complète des erreurs avec logs détaillés
        print(f"erreur dans generate-report: {str(e)}")
        print(traceback.format_exc())
        
        return jsonify({
            "error": "Internal server error",
            "details": str(e),
            "type": type(e).__name__
        }), 500

# export pour vercel
# vercel cherche automatiquement 'app' ou 'application'
# on exporte les deux pour être sûr
application = app

# pour le développement local (optionnel)
if __name__ == '__main__':
    print("demarrage en mode developpement local")
    app.run(debug=True, port=5000)
