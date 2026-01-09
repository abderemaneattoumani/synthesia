"""
route /api/health pour vercel
format handler simple et robuste
"""
import json
import sys
import os

# logs au chargement
print("=" * 60)
print("chargement api/health.py")
print("=" * 60)
print(f"python: {sys.version}")
print(f"cwd: {os.getcwd()}")
print(f"groq_key: {bool(os.environ.get('GROQ_API_KEY'))}")
print("=" * 60)

# handler vercel - format le plus simple
# vercel passe un objet request avec des attributs
def handler(request):
    """
    handler vercel pour /api/health
    format simple et robuste
    """
    try:
        print("handler health appelé")
        
        # méthode 1: essayer comme attribut
        try:
            method = request.method
            print(f"   method (attribut): {method}")
        except:
            # méthode 2: essayer comme dict
            try:
                method = request.get('method', 'GET') if isinstance(request, dict) else 'GET'
                print(f"   method (dict): {method}")
            except:
                # méthode 3: valeur par défaut
                method = 'GET'
                print(f"   method (défaut): {method}")
        
        # vérifier groq
        groq_ok = bool(os.environ.get('GROQ_API_KEY'))
        
        # réponse
        response = {
            "status": "online",
            "message": "SyntheSIA is running",
            "groq_configured": groq_ok
        }
        
        print(f"réponse: {response}")
        
        # retourner au format vercel
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(response, ensure_ascii=False)
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
