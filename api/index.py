"""
point d'entrée principal avec flask
version simple et robuste pour vercel
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

# créer l'app flask
app = Flask(__name__)
CORS(app)

# logs
print("=" * 60)
print("chargement api/index.py avec flask")
print("=" * 60)
print(f"python: {sys.version}")
print(f"cwd: {os.getcwd()}")
print(f"groq_key: {bool(os.environ.get('GROQ_API_KEY'))}")
print("=" * 60)

@app.route('/api/health', methods=['GET', 'OPTIONS'])
def health():
    """route health check"""
    try:
        print("route /api/health appelée")
        groq_ok = bool(os.environ.get('GROQ_API_KEY'))
        return jsonify({
            "status": "online",
            "message": "SyntheSIA is running",
            "groq_configured": groq_ok
        })
    except Exception as e:
        print(f"erreur health: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate-report', methods=['POST', 'OPTIONS'])
def generate_report():
    """route génération rapport"""
    try:
        print("route /api/generate-report appelée")
        
        # gestion options
        if request.method == 'OPTIONS':
            return '', 204
        
        # parser données
        data = request.get_json() or {}
        
        if not data.get('raw_data'):
            return jsonify({"error": "Missing raw_data"}), 400
        
        # extraire données
        title = data.get('title', 'Rapport')
        raw_data = data.get('raw_data', '')
        author = data.get('author', 'Anonyme')
        role = data.get('role', 'Technicien')
        
        print(f"données: titre={title}, auteur={author}, données={len(raw_data)} chars")
        
        # ajouter chemin pour imports
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        # importer utilitaires
        from utils.ai_handler import generate_summary
        from utils.pdf_generator import create_pdf
        from flask import send_file
        
        # générer résumé
        print("génération ia...")
        summary = generate_summary(raw_data)
        print(f"résumé ok ({len(summary)} chars)")
        
        # générer pdf
        print("génération pdf...")
        pdf_path = create_pdf(title, summary, author, role)
        print(f"pdf ok: {pdf_path}")
        
        # retourner pdf
        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='rapport.pdf'
        )
        
    except Exception as e:
        print(f"erreur generate-report: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

# export pour vercel
# vercel cherche une variable 'app' ou 'application'
application = app
