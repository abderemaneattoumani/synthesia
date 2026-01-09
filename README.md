# 🤖 SyntheSIA - Générateur de Rapports IA

Application web pour générer des rapports professionnels à partir de notes techniques, utilisant l'IA Groq (Llama 3.3) et générant des PDF avec ReportLab.

## 🚀 Déploiement sur Vercel

### Structure du Projet

```
synthesia/
├── api/
│   ├── index.py              # Point d'entrée Flask principal
│   └── utils/
│       ├── ai_handler.py     # Client Groq pour génération IA
│       └── pdf_generator.py   # Génération PDF avec ReportLab
├── public/
│   └── index.html            # Frontend (HTML + TailwindCSS)
├── vercel.json               # Configuration Vercel
├── requirements.txt          # Dépendances Python
└── .vercelignore            # Fichiers ignorés par Vercel
```

### Configuration Requise

1. **Variable d'environnement Vercel :**
   - `GROQ_API_KEY` : Votre clé API Groq
   - À ajouter dans : Vercel Dashboard → Settings → Environment Variables

2. **Dépendances Python :**
   - Toutes les dépendances sont dans `requirements.txt`
   - Installées automatiquement par Vercel lors du déploiement

### Déploiement

```bash
# 1. Cloner le projet
git clone <votre-repo>
cd synthesia

# 2. Vérifier les fichiers
ls api/index.py
ls public/index.html
ls vercel.json
ls requirements.txt

# 3. Déployer sur Vercel
vercel --prod

# Ou via Git (si connecté à Vercel)
git push origin main
```

### URLs de Production

- **Frontend :** https://synthesia-mu.vercel.app/
- **API Health :** https://synthesia-mu.vercel.app/api/health
- **API Generate :** https://synthesia-mu.vercel.app/api/generate-report

### Vérification

1. **Tester l'API Health :**
   ```bash
   curl https://synthesia-mu.vercel.app/api/health
   ```
   Devrait retourner :
   ```json
   {
     "status": "online",
     "message": "SyntheSIA API is running",
     "groq_configured": true
   }
   ```

2. **Tester le Frontend :**
   - Ouvrir https://synthesia-mu.vercel.app/
   - Remplir le formulaire
   - Générer un rapport

### Debug

- **Logs Vercel :** Dashboard → Functions → Logs
- **Erreurs courantes :**
  - 404 : Vérifier que `public/index.html` existe
  - 500 : Vérifier les logs et `GROQ_API_KEY`
  - Timeout : Vérifier la taille des fichiers (max 50mb)

## 🛠️ Développement Local

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
cd api
python index.py

# L'application sera disponible sur http://localhost:5000
```

## 📝 Fonctionnalités

- ✅ Génération de résumés avec IA Groq (Llama 3.3)
- ✅ Génération de PDF professionnels avec ReportLab
- ✅ Interface web moderne avec TailwindCSS
- ✅ Support CORS pour les requêtes cross-origin
- ✅ Gestion d'erreurs complète
- ✅ Logs détaillés pour debug

## 🔒 Sécurité

- ✅ Clé API Groq stockée dans les variables d'environnement Vercel
- ✅ Aucune clé API dans le code source
- ✅ Validation des données d'entrée
- ✅ Gestion sécurisée des fichiers temporaires (/tmp)

## 📦 Dépendances

- `flask==3.0.0` - Framework web
- `flask-cors==4.0.0` - Support CORS
- `groq==0.11.0` - Client API Groq
- `reportlab==4.0.7` - Génération PDF
- `Pillow==10.1.0` - Traitement d'images
- `httpx==0.27.0` - Client HTTP (dépendance Groq)

## 📄 Licence

Voir le fichier LICENSE

## 👤 Auteur

Abdérémane Attoumani

---

**Dernière mise à jour :** Structure optimisée pour Vercel avec Flask

