"""
route /api/generate-report pour vercel
format handler simple et robuste
"""
import json
import sys
import os
import base64

# logs au chargement
print("=" * 60)
print("chargement api/generate-report.py")
print("=" * 60)
print(f"python: {sys.version}")
print(f"cwd: {os.getcwd()}")
print(f"groq_key: {bool(os.environ.get('GROQ_API_KEY'))}")
print("=" * 60)

# handler vercel - format le plus simple
def handler(request):
    """
    handler vercel pour /api/generate-report
    format simple et robuste
    """
    try:
        print("handler generate-report appelé")
        
        # récupérer méthode http
        try:
            method = request.method
        except:
            try:
                method = request.get('method', 'POST') if isinstance(request, dict) else 'POST'
            except:
                method = 'POST'
        
        print(f"   method: {method}")
        
        # gestion options (cors)
        if method == 'OPTIONS':
            return {
                'statusCode': 204,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': ''
            }
        
        # vérifier post
        if method != 'POST':
            return {
                'statusCode': 405,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({"error": "Method not allowed"}, ensure_ascii=False)
            }
        
        # parser body
        try:
            if hasattr(request, 'body'):
                body_str = request.body
            elif isinstance(request, dict):
                body_str = request.get('body', '{}')
            else:
                body_str = getattr(request, 'body', '{}')
            
            # convertir bytes en string si nécessaire
            if isinstance(body_str, bytes):
                body_str = body_str.decode('utf-8')
            
            # parser json
            data = json.loads(body_str) if body_str else {}
            print(f"   données reçues: {list(data.keys()) if isinstance(data, dict) else 'pas un dict'}")
        except Exception as e:
            print(f"erreur parsing: {str(e)}")
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({"error": f"Invalid JSON: {str(e)}"}, ensure_ascii=False)
            }
        
        # validation
        if not data or not data.get('raw_data'):
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({"error": "Missing raw_data"}, ensure_ascii=False)
            }
        
        # extraire données
        title = data.get('title', 'Rapport')
        raw_data = data.get('raw_data', '')
        author = data.get('author', 'Anonyme')
        role = data.get('role', 'Technicien')
        
        print(f"   titre: {title}, auteur: {author}, données: {len(raw_data)} chars")
        
        # ajouter chemin pour imports
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        # importer utilitaires
        print("   import utilitaires...")
        from utils.ai_handler import generate_summary
        from utils.pdf_generator import create_pdf
        print("   utilitaires ok")
        
        # générer résumé ia
        print("   génération ia...")
        summary = generate_summary(raw_data)
        print(f"   résumé ok ({len(summary)} chars)")
        
        # générer pdf
        print("   génération pdf...")
        pdf_path = create_pdf(title, summary, author, role)
        print(f"   pdf ok: {pdf_path}")
        
        # lire pdf
        with open(pdf_path, 'rb') as f:
            pdf_bytes = f.read()
        
        # nettoyer
        try:
            os.remove(pdf_path)
        except:
            pass
        
        # encoder base64
        pdf_b64 = base64.b64encode(pdf_bytes).decode('utf-8')
        print(f"   pdf encodé ({len(pdf_b64)} chars)")
        
        # retourner
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/pdf',
                'Content-Disposition': 'attachment; filename="rapport.pdf"',
                'Access-Control-Allow-Origin': '*'
            },
            'body': pdf_b64,
            'isBase64Encoded': True
        }
        
    except Exception as e:
        print(f"ERREUR: {str(e)}")
        import traceback
        print(traceback.format_exc())
        
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                "error": str(e),
                "type": type(e).__name__
            }, ensure_ascii=False)
        }
