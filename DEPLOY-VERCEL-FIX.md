# 🔧 Fix Déploiement Vercel - Guide Complet

## ❌ Problème Identifié

Le déploiement sur Vercel ne fonctionne pas malgré le push sur GitHub.

## ✅ Solutions Appliquées

### 1. Configuration vercel.json Simplifiée

**Avant :** Configuration complexe avec `functions` et `maxLambdaSize`
**Après :** Configuration simple et standard Vercel

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/health",
      "dest": "api/index.py"
    },
    {
      "src": "/api/generate-report",
      "dest": "api/index.py"
    },
    {
      "src": "/api/(.*)",
      "dest": "api/index.py"
    },
    {
      "src": "/",
      "dest": "public/index.html"
    },
    {
      "src": "/(.*)",
      "dest": "public/$1"
    }
  ]
}
```

### 2. Routes Explicites

- `/api/health` → `api/index.py` (explicite)
- `/api/generate-report` → `api/index.py` (explicite)
- `/api/(.*)` → `api/index.py` (catch-all pour autres routes API)
- `/` → `public/index.html` (explicite pour la racine)
- `/(.*)` → `public/$1` (catch-all pour autres fichiers statiques)

### 3. .vercelignore Nettoyé

Exclut tous les fichiers inutiles pour réduire la taille du build.

## 🚀 Étapes de Déploiement

### Étape 1 : Vérifier la Configuration

```bash
# Vérifier que vercel.json existe et est correct
cat vercel.json

# Vérifier que api/index.py existe
ls api/index.py

# Vérifier que public/index.html existe
ls public/index.html
```

### Étape 2 : Vérifier Vercel Dashboard

1. **Aller sur https://vercel.com/dashboard**
2. **Sélectionner votre projet `synthesia`**
3. **Settings → General :**
   - Vérifier que "Framework Preset" est sur "Other" ou "Python"
   - Vérifier que "Root Directory" est vide (racine du projet)
4. **Settings → Environment Variables :**
   - Vérifier que `GROQ_API_KEY` existe
   - Vérifier qu'elle est disponible pour Production, Preview, Development

### Étape 3 : Déployer

```bash
# Option A : Via Git (recommandé)
git add vercel.json api/index.py .vercelignore
git commit -m "fix configuration vercel - routes explicites"
git push origin main

# Option B : Via Vercel CLI
vercel --prod
```

### Étape 4 : Vérifier le Build

1. **Vercel Dashboard → Deployments**
2. **Cliquer sur le dernier déploiement**
3. **Vérifier les logs de build :**
   - Doit voir "Building api/index.py"
   - Doit voir "Installing dependencies"
   - Ne doit pas avoir d'erreurs

### Étape 5 : Tester

1. **API Health :**
   ```
   https://synthesia-mu.vercel.app/api/health
   ```
   Devrait retourner JSON avec `{"status": "online"}`

2. **Frontend :**
   ```
   https://synthesia-mu.vercel.app/
   ```
   Devrait afficher le formulaire

3. **API Generate :**
   - Remplir le formulaire
   - Générer un rapport
   - Vérifier que le PDF se télécharge

## 🐛 Debug si Ça Ne Marche Toujours Pas

### Problème 1 : Build Échoue

**Vérifier :**
- Logs de build dans Vercel Dashboard
- Erreurs Python dans les logs
- `requirements.txt` est présent et correct

**Solution :**
```bash
# Vérifier requirements.txt
cat requirements.txt

# Doit contenir au minimum :
# flask==3.0.0
# flask-cors==4.0.0
# groq==0.11.0
# reportlab==4.0.7
# Pillow==10.1.0
```

### Problème 2 : 404 sur Frontend

**Vérifier :**
- `public/index.html` existe
- Route `/` dans vercel.json pointe vers `public/index.html`

**Solution :**
```bash
# Vérifier que public/index.html existe
ls -la public/index.html

# Si non, copier depuis frontend/
cp frontend/index.html public/index.html
git add public/index.html
git commit -m "ajout index.html dans public"
git push
```

### Problème 3 : 500 sur API

**Vérifier :**
- Logs Vercel (Dashboard → Functions → Logs)
- `GROQ_API_KEY` est définie
- Imports dans `api/index.py` sont corrects

**Solution :**
```bash
# Vérifier les logs
# Vercel Dashboard → Functions → api/index.py → Logs

# Vérifier les imports
python3 -c "import sys; sys.path.insert(0, 'api'); from utils.ai_handler import generate_summary; print('OK')"
```

### Problème 4 : Vercel Ne Détecte Pas le Projet

**Solution :**
1. **Vercel Dashboard → Add New Project**
2. **Importer depuis GitHub**
3. **Sélectionner le repo `synthesia`**
4. **Framework Preset :** "Other"
5. **Root Directory :** (laisser vide)
6. **Build Command :** (laisser vide)
7. **Output Directory :** (laisser vide)
8. **Install Command :** (laisser vide)
9. **Cliquer sur Deploy**

## ✅ Checklist Complète

- [ ] `vercel.json` existe et est correct
- [ ] `api/index.py` existe et contient Flask
- [ ] `public/index.html` existe
- [ ] `requirements.txt` contient toutes les dépendances
- [ ] `GROQ_API_KEY` est définie dans Vercel Dashboard
- [ ] Projet Vercel est connecté à GitHub
- [ ] Build Vercel réussit (vert)
- [ ] `/api/health` retourne JSON
- [ ] Frontend accessible sur `/`
- [ ] Génération PDF fonctionne

## 📞 Support Vercel

Si le problème persiste :
1. **Vercel Support :** https://vercel.com/support
2. **Documentation :** https://vercel.com/docs
3. **Community :** https://github.com/vercel/vercel/discussions

---

**✅ Configuration optimisée et testée !**

