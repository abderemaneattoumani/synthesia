"""
route /api/generate-report pour vercel
handler natif vercel python - pas de flask
"""
import json
import sys
import os
import base64
import tempfile

# logs au chargement du module
print("=" * 60)
print("chargement api/generate-report.py")
print("=" * 60)
print(f"python version: {sys.version}")
print(f"working directory: {os.getcwd()}")
print(f"groq_api_key configured: {bool(os.environ.get('GROQ_API_KEY'))}")
print("=" * 60)

def handler(request):
    """
    handler vercel natif pour /api/generate-report
    génère un pdf avec ia et le retourne en base64
    """
    try:
        print("handler generate-report appelé")
        
        # récupérer la méthode http (vercel peut passer request comme dict ou objet)
        if hasattr(request, 'method'):
            method = request.method
        elif isinstance(request, dict):
            method = request.get('method', 'POST')
        else:
            method = getattr(request, 'method', 'POST')
        
        print(f"   method: {method}")
        
        # gestion options (cors preflight)
        if method == 'OPTIONS':
            print("   options request - retour cors")
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
        
        # vérifier que c'est une requête post
        if method != 'POST':
            return {
                'statusCode': 405,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({"error": "Method not allowed"}, ensure_ascii=False)
            }
        
        # parser le body json
        # vercel peut passer le body de différentes façons
        try:
            if hasattr(request, 'body'):
                body = request.body
            elif isinstance(request, dict):
                body = request.get('body', '{}')
            else:
                body = getattr(request, 'body', '{}')
            
            # convertir en string si bytes
            if isinstance(body, bytes):
                body = body.decode('utf-8')
            
            # parser le json
            if isinstance(body, str):
                data = json.loads(body) if body else {}
            else:
                data = body if body else {}
            
            print(f"   body reçu: {list(data.keys()) if isinstance(data, dict) else 'not a dict'}")
        except Exception as e:
            print(f"erreur parsing json: {str(e)}")
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({"error": "Invalid JSON body", "details": str(e)}, ensure_ascii=False)
            }
        
        # validation des données
        if not data:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({"error": "No data provided"}, ensure_ascii=False)
            }
        
        # extraire les données du formulaire
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
        
        print(f"   titre: {title}")
        print(f"   auteur: {author}")
        print(f"   rôle: {role}")
        print(f"   données brutes: {len(raw_data)} caractères")
        
        # import des utilitaires (dans la fonction pour éviter les erreurs)
        print("   import des utilitaires...")
        # ajouter le chemin parent pour les imports
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        from utils.ai_handler import generate_summary
        from utils.pdf_generator import create_pdf
        print("   utilitaires importés")
        
        # génération du résumé ia
        print("   génération du résumé ia...")
        summary = generate_summary(raw_data)
        print(f"   résumé généré ({len(summary)} caractères)")
        
        # génération du pdf
        print("   génération du pdf...")
        pdf_path = create_pdf(title, summary, author, role)
        print(f"   pdf créé: {pdf_path}")
        
        # lire le pdf et le convertir en base64
        print("   lecture du pdf...")
        with open(pdf_path, 'rb') as f:
            pdf_bytes = f.read()
        
        # nettoyer le fichier temporaire
        try:
            os.remove(pdf_path)
            print(f"   fichier temporaire supprimé: {pdf_path}")
        except:
            print(f"   impossible de supprimer {pdf_path}")
        
        # encoder en base64
        pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
        print(f"   pdf encodé en base64 ({len(pdf_base64)} caractères)")
        
        # retourner le pdf
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
        # en cas d'erreur, logger et retourner une erreur 500
        print(f"erreur dans handler generate-report: {str(e)}")
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
