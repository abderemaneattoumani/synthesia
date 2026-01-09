# 🚀 Commandes Exactes pour Fix Vercel

## ✅ Corrections Appliquées

1. **vercel.json simplifié** - Routes explicites et standard
2. **api/index.py nettoyé** - Logs sans emojis (problèmes d'encodage)
3. **.vercelignore mis à jour** - Exclusion des fichiers inutiles

## 📋 Commandes Git Exactes

### Étape 1 : Vérifier les Changements

```bash
git status
```

Vous devriez voir :
- `vercel.json` (modifié)
- `api/index.py` (modifié)
- `.vercelignore` (modifié)
- `DEPLOY-VERCEL-FIX.md` (nouveau)
- `COMMANDES-FIX-VERCEL.md` (nouveau)

### Étape 2 : Ajouter les Fichiers

```bash
git add vercel.json api/index.py .vercelignore DEPLOY-VERCEL-FIX.md COMMANDES-FIX-VERCEL.md
```

**OU tout ajouter :**

```bash
git add .
```

### Étape 3 : Commit

```bash
git commit -m "fix vercel deployment - configuration simplifiee et routes explicites

- vercel.json: routes explicites pour api et frontend
- api/index.py: logs nettoyes (sans emojis)
- .vercelignore: exclusion fichiers inutiles
- configuration optimisee pour detection automatique vercel"
```

### Étape 4 : Push

```bash
git push origin main
```

## ⚙️ Configuration Vercel Dashboard

### IMPORTANT : Vérifier ces Paramètres

1. **Aller sur https://vercel.com/dashboard**
2. **Sélectionner votre projet `synthesia`**
3. **Settings → General :**
   - **Framework Preset :** "Other" (ou laisser vide)
   - **Root Directory :** (laisser VIDE - racine du projet)
   - **Build Command :** (laisser VIDE)
   - **Output Directory :** (laisser VIDE)
   - **Install Command :** (laisser VIDE)

4. **Settings → Environment Variables :**
   - Vérifier que `GROQ_API_KEY` existe
   - Vérifier qu'elle est disponible pour ✅ Production, ✅ Preview, ✅ Development

5. **Settings → Git :**
   - Vérifier que le repo GitHub est connecté
   - Vérifier que la branche `main` (ou `master`) est sélectionnée

## ✅ Vérifications Après Push

### 1. Attendre le Build (2-5 minutes)

- **Vercel Dashboard → Deployments**
- Cliquer sur le dernier déploiement
- Vérifier que le build est **vert** (succès)
- Vérifier les logs de build :
  - Doit voir "Building api/index.py"
  - Doit voir "Installing dependencies from requirements.txt"
  - Ne doit pas avoir d'erreurs

### 2. Tester l'API Health

**Dans le navigateur ou avec curl :**
```
https://synthesia-mu.vercel.app/api/health
```

**Résultat attendu :**
```json
{
  "status": "online",
  "message": "SyntheSIA API is running",
  "groq_configured": true,
  "environment": "production"
}
```

### 3. Tester le Frontend

**Dans le navigateur :**
```
https://synthesia-mu.vercel.app/
```

**Résultat attendu :**
- Formulaire visible
- Pas d'erreur 404
- Pas d'erreur dans la console (F12)

### 4. Tester la Génération PDF

1. Remplir le formulaire :
   - Titre : "Test Rapport"
   - Nom : "Test"
   - Poste : "Testeur"
   - Notes : "Test de génération de rapport avec IA"

2. Cliquer sur "Générer le rapport PDF"

3. Vérifier :
   - Le PDF se télécharge
   - Pas d'erreur dans la console
   - Pas d'erreur dans les logs Vercel

### 5. Vérifier les Logs Vercel

1. **Vercel Dashboard → Project → Functions → api/index.py → Logs**
2. Vérifier qu'il n'y a pas d'erreurs
3. Voir les prints de debug :
   - "SYNTHESIA API - DEMARRAGE"
   - "route /api/health appelee"
   - etc.

## 🐛 Si Ça Ne Marche Toujours Pas

### Problème : Build Échoue

**Vérifier :**
- Logs de build dans Vercel Dashboard
- Erreurs dans les logs
- `requirements.txt` est présent

**Solution :**
```bash
# Vérifier requirements.txt
cat requirements.txt

# Doit contenir :
# flask==3.0.0
# flask-cors==4.0.0
# groq==0.11.0
# reportlab==4.0.7
# Pillow==10.1.0
# httpx==0.27.0
# python-dotenv==1.0.0
```

### Problème : 404 sur Frontend

**Vérifier :**
- `public/index.html` existe
- Route `/` dans vercel.json

**Solution :**
```bash
# Vérifier
ls -la public/index.html

# Si manquant
cp frontend/index.html public/index.html
git add public/index.html
git commit -m "ajout index.html dans public"
git push
```

### Problème : 500 sur API

**Vérifier :**
- Logs Vercel (Dashboard → Functions → Logs)
- `GROQ_API_KEY` est définie
- Imports dans `api/index.py`

**Solution :**
1. Vérifier les logs Vercel
2. Vérifier `GROQ_API_KEY` dans Vercel Dashboard
3. Vérifier les imports :
```bash
cd api
python3 -c "from utils.ai_handler import generate_summary; print('OK')"
```

### Problème : Vercel Ne Détecte Pas le Projet

**Solution :**
1. **Vercel Dashboard → Add New Project**
2. **Importer depuis GitHub**
3. **Sélectionner le repo `synthesia`**
4. **Configuration :**
   - Framework Preset : "Other"
   - Root Directory : (vide)
   - Build Command : (vide)
   - Output Directory : (vide)
   - Install Command : (vide)
5. **Environment Variables :**
   - Ajouter `GROQ_API_KEY`
6. **Cliquer sur Deploy**

## 📊 Structure Finale

```
synthesia/
├── api/
│   ├── index.py              ✅ Point d'entrée Flask
│   └── utils/
│       ├── ai_handler.py     ✅ Client Groq
│       └── pdf_generator.py   ✅ Génération PDF
├── public/
│   └── index.html            ✅ Frontend
├── vercel.json               ✅ Configuration simplifiée
├── requirements.txt           ✅ Dépendances
├── .vercelignore            ✅ Fichiers ignorés
└── README.md                ✅ Documentation
```

## ✅ Checklist Complète

- [ ] `vercel.json` existe et contient les routes explicites
- [ ] `api/index.py` existe et contient Flask
- [ ] `public/index.html` existe
- [ ] `requirements.txt` contient toutes les dépendances
- [ ] `GROQ_API_KEY` est définie dans Vercel Dashboard
- [ ] Projet Vercel est connecté à GitHub
- [ ] Framework Preset est sur "Other" ou vide
- [ ] Root Directory est vide
- [ ] Build Vercel réussit (vert)
- [ ] `/api/health` retourne JSON
- [ ] Frontend accessible sur `/`
- [ ] Génération PDF fonctionne

## 🎯 Prochaines Étapes

1. ✅ Exécuter les commandes Git ci-dessus
2. ✅ Vérifier la configuration Vercel Dashboard
3. ✅ Attendre le build (2-5 minutes)
4. ✅ Tester toutes les URLs
5. ✅ Vérifier les logs si problème

---

**✅ Configuration corrigée et optimisée pour Vercel !**

