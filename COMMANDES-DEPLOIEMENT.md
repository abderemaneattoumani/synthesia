# 📋 Commandes Exactes pour Déploiement

## ✅ Structure Optimale Créée

Le projet a été **complètement restructuré** pour un hébergement optimal sur Vercel.

## 🚀 Commandes Git Exactes

### Étape 1 : Vérifier les Changements

```bash
git status
```

Vous devriez voir :
- `api/index.py` (modifié - Flask optimisé)
- `vercel.json` (modifié - configuration optimale)
- `public/index.html` (existe)
- `requirements.txt` (modifié - Flask ajouté)
- `.vercelignore` (nouveau)
- `README.md` (nouveau)
- `DEPLOY-FINAL.md` (nouveau)

### Étape 2 : Ajouter Tous les Fichiers

```bash
git add .
```

**OU sélectivement :**

```bash
git add api/index.py
git add vercel.json
git add public/index.html
git add requirements.txt
git add .vercelignore
git add README.md
git add DEPLOY-FINAL.md
git add COMMANDES-DEPLOIEMENT.md
```

### Étape 3 : Commit

```bash
git commit -m "restructuration complète - flask optimisé pour vercel

- point d'entrée unique api/index.py avec flask
- configuration vercel.json optimisée (50mb, 60s timeout)
- frontend dans public/ (standard vercel)
- tous les imports corrigés et vérifiés
- logs détaillés pour debug
- documentation complète ajoutée
- structure propre et professionnelle"
```

### Étape 4 : Push vers GitHub

```bash
git push origin main
```

**OU si votre branche principale s'appelle `master` :**

```bash
git push origin master
```

## ⚙️ Configuration Vercel (IMPORTANT)

### Avant le Push : Vérifier la Variable d'Environnement

1. Aller sur https://vercel.com/dashboard
2. Sélectionner votre projet `synthesia`
3. **Settings** → **Environment Variables**
4. Vérifier que `GROQ_API_KEY` existe
5. Si elle n'existe pas, l'ajouter :
   - **Name:** `GROQ_API_KEY`
   - **Value:** Votre clé API Groq
   - **Environments:** ✅ Production, ✅ Preview, ✅ Development

## ✅ Vérifications Après Déploiement

### 1. Attendre le Build (2-5 minutes)

- Vérifier dans Vercel Dashboard → Deployments
- Le build doit être vert (succès)

### 2. Tester l'API Health

```bash
curl https://synthesia-mu.vercel.app/api/health
```

**OU ouvrir dans le navigateur :**
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

Ouvrir dans le navigateur :
```
https://synthesia-mu.vercel.app/
```

**Résultat attendu :**
- Formulaire visible
- Pas d'erreur 404

### 4. Tester la Génération PDF

1. Remplir le formulaire :
   - Titre : "Test Rapport"
   - Nom : "Test"
   - Poste : "Testeur"
   - Notes : "Test de génération de rapport"

2. Cliquer sur "Générer le rapport PDF"

3. Vérifier :
   - Le PDF se télécharge
   - Pas d'erreur dans la console

### 5. Vérifier les Logs Vercel

1. Vercel Dashboard → Project → Functions → Logs
2. Vérifier qu'il n'y a pas d'erreurs
3. Voir les prints de debug

## 🐛 Si Ça Ne Marche Pas

### Problème : Frontend 404

**Solution :**
```bash
# Vérifier que public/index.html existe
ls public/index.html

# Si non, copier depuis frontend/
cp frontend/index.html public/index.html
git add public/index.html
git commit -m "ajout index.html dans public"
git push
```

### Problème : API 500

**Solution :**
1. Vérifier les logs Vercel (Dashboard → Functions → Logs)
2. Vérifier que `GROQ_API_KEY` est définie
3. Vérifier les imports dans `api/index.py`

### Problème : "ModuleNotFoundError"

**Solution :**
```bash
# Vérifier la structure
ls api/utils/ai_handler.py
ls api/utils/pdf_generator.py

# Si manquant, vérifier les chemins d'import
```

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
├── vercel.json               ✅ Configuration optimale
├── requirements.txt           ✅ Dépendances
├── .vercelignore            ✅ Fichiers ignorés
└── README.md                ✅ Documentation
```

## 🎯 Checklist Avant Push

- [ ] `api/index.py` existe et contient Flask
- [ ] `vercel.json` est correctement configuré
- [ ] `public/index.html` existe
- [ ] `requirements.txt` contient Flask
- [ ] `GROQ_API_KEY` est définie dans Vercel Dashboard
- [ ] Tous les fichiers sont ajoutés (`git status` propre)

## 🚀 Après le Push

1. **Surveiller le build** dans Vercel Dashboard
2. **Tester `/api/health`** dès que le déploiement est terminé
3. **Tester le frontend** sur `/`
4. **Vérifier les logs** pour s'assurer qu'il n'y a pas d'erreurs

---

**✅ Tout est prêt pour le déploiement !**

