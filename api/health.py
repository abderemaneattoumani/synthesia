"""
Route /api/health pour Vercel
Handler natif Vercel Python - pas de Flask
"""
import json
import sys
import os

print("=" * 60)
print("🚀 CHARGEMENT api/health.py")
print("=" * 60)
print(f"Python version: {sys.version}")
print(f"Working directory: {os.getcwd()}")
print(f"GROQ_API_KEY configured: {bool(os.environ.get('GROQ_API_KEY'))}")
print("=" * 60)

def handler(request):
    """
    Handler Vercel natif pour /api/health
    Accepte un objet Request de Vercel et retourne une Response
    """
    try:
        print("✅ Handler health appelé")
        print(f"   Method: {request.method}")
        print(f"   Path: {request.path}")
        print(f"   Headers: {dict(request.headers)}")
        
        # Vérifier la clé API Groq
        groq_configured = bool(os.environ.get('GROQ_API_KEY'))
        
        response_data = {
            "status": "online",
            "message": "SyntheSIA is running",
            "groq_configured": groq_configured,
            "environment": "production" if os.environ.get('VERCEL') else "development"
        }
        
        print(f"✅ Réponse générée: {response_data}")
        
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
        print(f"❌ ERREUR dans handler health: {str(e)}")
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

