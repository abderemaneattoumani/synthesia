print("========================================")
print("🚀 DÉBUT CHARGEMENT api/index.py")
print("========================================")

try:
    print("📦 Import Flask...")
    from flask import Flask, request, jsonify, send_file
    print("✅ Flask importé")
    
    print("📦 Import CORS...")
    from flask_cors import CORS
    print("✅ CORS importé")
    
    print("📦 Import datetime...")
    from datetime import datetime
    print("✅ datetime importé")
    
    print("📦 Import os, sys...")
    import os
    import sys
    print("✅ os, sys importés")
    
    print("📦 Configuration sys.path...")
    sys.path.insert(0, os.path.dirname(__file__))
    print(f"✅ sys.path[0] = {sys.path[0]}")
    
    print("📦 Import generate_summary...")
    from utils.ai_handler import generate_summary
    print("✅ generate_summary importé")
    
    print("📦 Import create_pdf...")
    from utils.pdf_generator import create_pdf
    print("✅ create_pdf importé")
    
    print("========================================")
    print("✅ TOUS LES IMPORTS RÉUSSIS")
    print("========================================")
    
except Exception as e:
    print("========================================")
    print(f"❌ ERREUR LORS DES IMPORTS: {e}")
    print("========================================")
    import traceback
    traceback.print_exc()
    raise

# Initialisation Flask
print("🔧 Initialisation Flask...")
app = Flask(__name__)
print("✅ Flask initialisé")

# Configuration CORS
print("🔧 Configuration CORS...")
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})
print("✅ CORS configuré")

# Route de santé
@app.route('/api/health', methods=['GET'])
def health():
    """Endpoint de vérification"""
    print("🏥 Route /api/health appelée")
    return jsonify({
        "status": "online",
        "message": "SyntheSIA API fonctionne !",
        "timestamp": datetime.now().isoformat(),
        "groq_key_configured": bool(os.environ.get('GROQ_API_KEY')),
        "python_version": sys.version
    }), 200

@app.route('/api/', methods=['GET'])
def index():
    """Page d'accueil de l'API"""
    print("🏠 Route /api/ appelée")
    return jsonify({
        "name": "SyntheSIA API",
        "version": "1.0",
        "endpoints": {
            "health": "/api/health",
            "generate": "/api/generate-report"
        }
    }), 200

# Route de génération
@app.route('/api/generate-report', methods=['POST', 'OPTIONS'])
def generate_report():
    """Génère un rapport PDF"""
    print("📝 Route /api/generate-report appelée")
    
    if request.method == 'OPTIONS':
        print("✅ Requête OPTIONS (CORS preflight)")
        return '', 204
    
    try:
        print("📥 Récupération des données...")
        data = request.get_json()
        
        if not data:
            print("❌ Aucune donnée JSON reçue")
            return jsonify({"error": "Aucune donnée reçue"}), 400
        
        title = data.get('title', 'Rapport sans titre')
        raw_data = data.get('raw_data', '')
        author = data.get('author', 'Anonyme')
        role = data.get('role', 'Non spécifié')
        
        print(f"📋 Titre: {title}")
        print(f"👤 Auteur: {author} ({role})")
        print(f"📝 Données brutes: {len(raw_data)} caractères")
        
        if not raw_data:
            print("❌ Le champ raw_data est vide")
            return jsonify({"error": "Le champ 'raw_data' est requis"}), 400
        
        print("🤖 Appel à generate_summary...")
        summary = generate_summary(raw_data)
        print(f"✅ Résumé généré: {len(summary)} caractères")
        
        print("📄 Appel à create_pdf...")
        pdf_path = create_pdf(title, summary, author, role)
        print(f"✅ PDF créé: {pdf_path}")
        
        print("📤 Envoi du PDF...")
        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"rapport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
        
    except Exception as e:
        print(f"❌ ERREUR dans generate_report: {e}")
        import traceback
        error_trace = traceback.format_exc()
        print(error_trace)
        return jsonify({
            "error": str(e),
            "trace": error_trace
        }), 500

print("========================================")
print("✅ CONFIGURATION COMPLÈTE")
print("========================================")

# Export pour Vercel
handler = app

if __name__ == '__main__':
    print("🖥️  Lancement en mode développement local")
    app.run(debug=True, port=5000)