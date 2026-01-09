import os

def generate_summary(raw_text):
    """Génère un résumé avec Groq AI"""
    try:
        # ═══════════════════════════════════════════════════════
        # IMPORT GROQ ICI (pas au niveau module)
        # ═══════════════════════════════════════════════════════
        from groq import Groq
        
        # Récupérer la clé API
        api_key = os.environ.get('GROQ_API_KEY')
        
        if not api_key:
            return "ERREUR: Clé API Groq non configurée dans les variables d'environnement Vercel"
        
        # ═══════════════════════════════════════════════════════
        # INITIALISER LE CLIENT ICI (pas au niveau module)
        # ═══════════════════════════════════════════════════════
        client = Groq(api_key=api_key)
        
        # Prompt pour l'IA
        system_prompt = """Tu es un assistant expert qui transforme des notes techniques 
        en rapports professionnels de qualité. Tu dois structurer le contenu en sections claires :
        
        - CONTEXTE DE L'INTERVENTION
        - PROBLEMATIQUE IDENTIFIEE  
        - ACTIONS TECHNIQUES REALISEES
        - RESULTATS OBTENUS
        - RECOMMANDATIONS
        
        Utilise un ton professionnel et précis. Ne mets PAS d'emojis."""
        
        # Appel à l'API Groq
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Transforme ces notes techniques en rapport professionnel structuré :\n\n{raw_text}"}
            ],
            max_tokens=800,
            temperature=0.7
        )
        
        # Extraire le résumé
        summary = response.choices[0].message.content
        
        print(f"✅ Résumé IA généré avec succès ({len(summary)} caractères)")
        return summary
        
    except Exception as e:
        error_msg = f"Erreur lors de la génération IA : {str(e)}"
        print(f"❌ {error_msg}")
        
        # Retourner un message d'erreur détaillé
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