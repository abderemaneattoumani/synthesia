"""
générateur de résumé avec groq ai
"""
import os

def generate_summary(raw_text):
    """
    génère un résumé avec groq ai
    param raw_text: texte brut à transformer en rapport
    return: texte du rapport généré par l'ia
    """
    try:
        # import groq ici (pas au niveau module pour éviter les erreurs au chargement)
        from groq import Groq
        
        # récupérer la clé api depuis les variables d'environnement
        api_key = os.environ.get('GROQ_API_KEY')
        
        # vérifier que la clé est configurée
        if not api_key:
            return "ERREUR: Clé API Groq non configurée dans les variables d'environnement Vercel"
        
        # initialiser le client groq ici (pas au niveau module)
        client = Groq(api_key=api_key)
        
        # prompt système pour guider l'ia
        system_prompt = """Tu es un assistant expert qui transforme des notes techniques 
        en rapports professionnels de qualité. Tu dois structurer le contenu en sections claires :
        
        - CONTEXTE DE L'INTERVENTION
        - PROBLEMATIQUE IDENTIFIEE  
        - ACTIONS TECHNIQUES REALISEES
        - RESULTATS OBTENUS
        - RECOMMANDATIONS
        
        Utilise un ton professionnel et précis. Ne mets PAS d'emojis."""
        
        # appel à l'api groq pour générer le résumé
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Transforme ces notes techniques en rapport professionnel structuré :\n\n{raw_text}"}
            ],
            max_tokens=800,
            temperature=0.7
        )
        
        # extraire le résumé de la réponse
        summary = response.choices[0].message.content
        
        print(f"résumé ia généré avec succès ({len(summary)} caractères)")
        return summary
        
    except Exception as e:
        # en cas d'erreur, logger et retourner un message d'erreur
        error_msg = f"Erreur lors de la génération IA : {str(e)}"
        print(f"erreur: {error_msg}")
        
        # retourner un message d'erreur détaillé pour l'utilisateur
        return f"""ERREUR DE GENERATION IA

Le système n'a pas pu générer le résumé automatique.

Détails techniques : {str(e)}

Veuillez vérifier :
1. La configuration de la clé API Groq dans Vercel
2. Votre connexion internet
3. Le quota de votre compte Groq

Les notes brutes sont ci-dessous :

{raw_text}
"""
