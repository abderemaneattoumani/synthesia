"""
test handler le plus simple possible
pour vérifier que vercel fonctionne
"""
import json

def handler(request):
    """
    handler ultra simple pour test
    """
    print("test-simple handler appelé")
    
    # retourner directement
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            "status": "ok",
            "message": "test simple fonctionne"
        })
    }

