from groq import Groq
import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# Initialisation du client Groq (IA GRATUITE)
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def generate_summary(raw_text):
    """
    Utilise Groq (IA gratuite) pour transformer du texte brut en résumé professionnel
    
    Args:
        raw_text (str): Notes techniques brutes
        
    Returns:
        str: Résumé structuré et professionnel
    """
    
    # Prompt optimisé pour générer un rapport technique
    system_prompt = """Tu es un assistant expert qui transforme des notes techniques 
    en rapports professionnels de qualité. Tu dois :
    
    - Structurer l'information de manière claire et logique
    - Utiliser un ton professionnel et précis
    - Organiser le contenu en sections : 
      * Contexte de l'intervention
      * Problématique identifiée
      * Actions techniques réalisées
      * Résultats obtenus
      * Recommandations
    - Garder une longueur de 250-350 mots
    - Utiliser des emojis professionnels pour les titres (📋 🎯 ⚙️ ✅ 💡)
    
    Le rapport doit être adapté pour être lu par un responsable technique."""
    
    try:
        # Appel à l'API Groq (GRATUIT et RAPIDE)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Modèle gratuit ultra-performant
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Transforme ces notes techniques en rapport professionnel structuré :\n\n{raw_text}"}
            ],
            max_tokens=800,  # Permet des rapports détaillés
            temperature=0.7  # Bon équilibre créativité/précision
        )
        
        # Extraction du texte généré
        summary = response.choices[0].message.content
        
        print(f"✅ Résumé IA généré avec succès ({len(summary)} caractères)")
        return summary
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Erreur Groq : {error_msg}")
        
        # Message d'erreur plus clair
        if "api_key" in error_msg.lower():
            return """
❌ ERREUR DE CONFIGURATION

La clé API Groq n'est pas configurée correctement.
GROQ_API_KEY=votre_clé dans le fichier .env

            """
        else:
            return f"❌ Erreur lors de la génération du rapport : {error_msg}"