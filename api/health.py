"""
route /api/health pour vercel
handler natif vercel python - pas de flask
"""
import json
import sys
import os

# logs au chargement du module
print("=" * 60)
print("chargement api/health.py")
print("=" * 60)
print(f"python version: {sys.version}")
print(f"working directory: {os.getcwd()}")
print(f"groq_api_key configured: {bool(os.environ.get('GROQ_API_KEY'))}")
print("=" * 60)

def handler(request):
    """
    handler vercel natif pour /api/health
    accepte un objet request de vercel et retourne une réponse
    """
    try:
        print("handler health appelé")
        
        # récupérer la méthode http (get, post, etc.)
        # vercel peut passer request comme dict ou objet
        if hasattr(request, 'method'):
            method = request.method
        elif isinstance(request, dict):
            method = request.get('method', 'GET')
        else:
            method = getattr(request, 'method', 'GET')
        
        print(f"   method: {method}")
        
        # vérifier la clé api groq dans les variables d'environnement
        groq_configured = bool(os.environ.get('GROQ_API_KEY'))
        
        # préparer la réponse json
        response_data = {
            "status": "online",
            "message": "SyntheSIA is running",
            "groq_configured": groq_configured,
            "environment": "production" if os.environ.get('VERCEL') else "development"
        }
        
        print(f"réponse générée: {response_data}")
        
        # retourner la réponse au format vercel
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(response_data, ensure_ascii=False)
        }
        
    except Exception as e:
        # en cas d'erreur, logger et retourner une erreur 500
        print(f"erreur dans handler health: {str(e)}")
        import traceback
        print(traceback.format_exc())
        
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                "error": "Internal server error",
                "details": str(e)
            }, ensure_ascii=False)
        }
