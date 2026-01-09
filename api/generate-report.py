"""
Route /api/generate-report pour Vercel
Handler natif Vercel Python - pas de Flask
"""
import json
import sys
import os
import base64
import tempfile

print("=" * 60)
print("🚀 CHARGEMENT api/generate-report.py")
print("=" * 60)
print(f"Python version: {sys.version}")
print(f"Working directory: {os.getcwd()}")
print(f"GROQ_API_KEY configured: {bool(os.environ.get('GROQ_API_KEY'))}")
print("=" * 60)

def handler(request):
    """
    Handler Vercel natif pour /api/generate-report
    Génère un PDF avec IA et le retourne en base64
    """
    try:
        print("✅ Handler generate-report appelé")
        print(f"   Method: {request.method}")
        print(f"   Path: {request.path}")
        
        # Gestion OPTIONS (CORS preflight)
        if request.method == 'OPTIONS':
            print("   OPTIONS request - retour CORS")
            return {
                'statusCode': 204,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Max-Age': '3600'
                },
                'body': ''
            }
        
        # Vérifier que c'est une requête POST
        if request.method != 'POST':
            return {
                'statusCode': 405,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({"error": "Method not allowed"}, ensure_ascii=False)
            }
        
        # Parser le body JSON
        try:
            body = request.body
            if isinstance(body, str):
                data = json.loads(body)
            elif isinstance(body, bytes):
                data = json.loads(body.decode('utf-8'))
            else:
                data = body if body else {}
            
            print(f"   Body reçu: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
        except Exception as e:
            print(f"❌ Erreur parsing JSON: {str(e)}")
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({"error": "Invalid JSON body", "details": str(e)}, ensure_ascii=False)
            }
        
        # Validation des données
        if not data:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({"error": "No data provided"}, ensure_ascii=False)
            }
        
        title = data.get('title', 'Rapport')
        raw_data = data.get('raw_data', '')
        author = data.get('author', 'Anonyme')
        role = data.get('role', 'Technicien')
        
        if not raw_data:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({"error": "Missing raw_data"}, ensure_ascii=False)
            }
        
        print(f"   Titre: {title}")
        print(f"   Auteur: {author}")
        print(f"   Rôle: {role}")
        print(f"   Données brutes: {len(raw_data)} caractères")
        
        # ═══════════════════════════════════════════════════════
        # IMPORT DES UTILITAIRES (dans la fonction pour éviter les erreurs)
        # ═══════════════════════════════════════════════════════
        print("   Import des utilitaires...")
        # Ajouter le chemin parent pour les imports
        import sys
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        from utils.ai_handler import generate_summary
        from utils.pdf_generator import create_pdf
        print("   ✅ Utilitaires importés")
        
        # Génération du résumé IA
        print("   Génération du résumé IA...")
        summary = generate_summary(raw_data)
        print(f"   ✅ Résumé généré ({len(summary)} caractères)")
        
        # Génération du PDF
        print("   Génération du PDF...")
        pdf_path = create_pdf(title, summary, author, role)
        print(f"   ✅ PDF créé: {pdf_path}")
        
        # Lire le PDF et le convertir en base64
        print("   Lecture du PDF...")
        with open(pdf_path, 'rb') as f:
            pdf_bytes = f.read()
        
        # Nettoyer le fichier temporaire
        try:
            os.remove(pdf_path)
            print(f"   ✅ Fichier temporaire supprimé: {pdf_path}")
        except:
            print(f"   ⚠️  Impossible de supprimer {pdf_path}")
        
        # Encoder en base64
        pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
        print(f"   ✅ PDF encodé en base64 ({len(pdf_base64)} caractères)")
        
        # Retourner le PDF
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/pdf',
                'Content-Disposition': f'attachment; filename="rapport_{os.path.basename(pdf_path)}"',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Expose-Headers': 'Content-Disposition'
            },
            'body': pdf_base64,
            'isBase64Encoded': True
        }
        
    except Exception as e:
        print(f"❌ ERREUR dans handler generate-report: {str(e)}")
        import traceback
        error_trace = traceback.format_exc()
        print(error_trace)
        
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                "error": "Internal server error",
                "details": str(e),
                "traceback": error_trace if os.environ.get('VERCEL_ENV') != 'production' else None
            }, ensure_ascii=False)
        }

