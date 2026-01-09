from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from datetime import datetime
import os
import sys

# Configuration du path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Imports
from utils.ai_handler import generate_summary
from utils.pdf_generator import create_pdf

# Application Flask
app = Flask(__name__)
CORS(app)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "online",
        "message": "SyntheSIA is running",
        "groq_configured": bool(os.environ.get('GROQ_API_KEY'))
    })

@app.route('/api/generate-report', methods=['POST', 'OPTIONS'])
def generate_report():
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data"}), 400
        
        title = data.get('title', 'Rapport')
        raw_data = data.get('raw_data', '')
        author = data.get('author', 'Anonyme')
        role = data.get('role', 'Technicien')
        
        if not raw_data:
            return jsonify({"error": "Missing raw_data"}), 400
        
        summary = generate_summary(raw_data)
        pdf_path = create_pdf(title, summary, author, role)
        
        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"rapport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# CRITICAL: Point d'entrée pour Vercel
def handler(event, context):
    """
    Handler serverless pour Vercel
    Convertit les événements Vercel en requêtes WSGI
    """
    from werkzeug.wrappers import Request, Response
    from io import BytesIO
    
    # Construire la requête WSGI depuis l'événement Vercel
    environ = {
        'REQUEST_METHOD': event.get('httpMethod', 'GET'),
        'PATH_INFO': event.get('path', '/'),
        'QUERY_STRING': event.get('queryStringParameters', ''),
        'CONTENT_TYPE': event.get('headers', {}).get('content-type', ''),
        'CONTENT_LENGTH': len(event.get('body', '')),
        'wsgi.input': BytesIO(event.get('body', '').encode()),
        'wsgi.errors': sys.stderr,
        'wsgi.version': (1, 0),
        'wsgi.multithread': False,
        'wsgi.multiprocess': True,
        'wsgi.run_once': False,
        'wsgi.url_scheme': 'https',
        'SERVER_NAME': 'vercel',
        'SERVER_PORT': '443',
    }
    
    # Ajouter les headers
    for key, value in event.get('headers', {}).items():
        key = 'HTTP_' + key.upper().replace('-', '_')
        environ[key] = value
    
    # Appeler l'app Flask
    response = Response.from_app(app, environ)
    
    return {
        'statusCode': response.status_code,
        'headers': dict(response.headers),
        'body': response.get_data(as_text=True)
    }