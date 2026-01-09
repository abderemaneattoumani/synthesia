# 🚀 Guide de Déploiement Final - SyntheSIA

## ✅ Structure Optimale Créée

Le projet a été **complètement restructuré** pour un hébergement optimal sur Vercel :

### Structure Finale

```
synthesia/
├── api/
│   ├── index.py              ✅ Point d'entrée Flask unique
│   └── utils/
│       ├── ai_handler.py     ✅ Client Groq
│       └── pdf_generator.py   ✅ Génération PDF (/tmp)
├── public/
│   └── index.html            ✅ Frontend
├── vercel.json               ✅ Configuration optimale
├── requirements.txt           ✅ Toutes les dépendances
├── .vercelignore            ✅ Fichiers ignorés
└── README.md                ✅ Documentation
```

## 🎯 Solution Implémentée : Flask avec Point d'Entrée Unique

**Pourquoi cette solution ?**
- ✅ Meilleur support Vercel pour Flask
- ✅ Point d'entrée unique (`api/index.py`)
- ✅ Routes Flask standard et maintenables
- ✅ Configuration simple et robuste
- ✅ Logs détaillés pour debug

## 📋 Étapes de Déploiement

### Étape 1 : Vérifier les Fichiers

```bash
# Vérifier la structure
ls api/index.py          # Doit exister
ls public/index.html      # Doit exister
ls vercel.json            # Doit exister
ls requirements.txt       # Doit exister
```

### Étape 2 : Configurer la Variable d'Environnement

1. Aller sur https://vercel.com/dashboard
2. Sélectionner votre projet `synthesia`
3. Settings → Environment Variables
4. Ajouter :
   - **Name:** `GROQ_API_KEY`
   - **Value:** Votre clé API Groq
   - **Environments:** Production, Preview, Development (tous)

### Étape 3 : Déployer

```bash
# Option A : Via Git (recommandé)
git add .
git commit -m "restructuration complète - flask optimisé"
git push origin main

# Option B : Via Vercel CLI
vercel --prod
```

### Étape 4 : Vérifier le Déploiement

1. **Attendre le build** (2-5 minutes)
   - Vérifier dans Vercel Dashboard → Deployments

2. **Tester l'API Health :**
   ```
   https://synthesia-mu.vercel.app/api/health
   ```
   Devrait retourner :
   ```json
   {
     "status": "online",
     "message": "SyntheSIA API is running",
     "groq_configured": true
   }
   ```

3. **Tester le Frontend :**
   ```
   https://synthesia-mu.vercel.app/
   ```
   Devrait afficher le formulaire

4. **Tester la Génération PDF :**
   - Remplir le formulaire
   - Cliquer sur "Générer le rapport PDF"
   - Vérifier que le PDF se télécharge

## 🔍 Debug et Logs

### Voir les Logs Vercel

1. **Via Dashboard :**
   - Vercel Dashboard → Project → Functions → Logs
   - Voir tous les prints de debug

2. **Via CLI :**
   ```bash
   vercel logs
   ```

### Erreurs Courantes

#### 1. Frontend 404
**Cause :** `public/index.html` manquant ou mal configuré
**Solution :** Vérifier que `public/index.html` existe

#### 2. API 500
**Cause :** Erreur Python dans le handler
**Solution :** Vérifier les logs Vercel pour voir l'erreur exacte

#### 3. "GROQ_API_KEY not configured"
**Cause :** Variable d'environnement manquante
**Solution :** Ajouter `GROQ_API_KEY` dans Vercel Dashboard

#### 4. "ModuleNotFoundError"
**Cause :** Import incorrect
**Solution :** Vérifier que `api/utils/` existe et contient les fichiers

#### 5. Timeout
**Cause :** Génération IA trop longue
**Solution :** Vérifier les limites Vercel (maxDuration: 60s configuré)

## ✅ Checklist Post-Déploiement

- [ ] `/api/health` retourne `{"status": "online"}`
- [ ] `groq_configured: true` dans la réponse health
- [ ] Frontend accessible sur `/`
- [ ] Formulaire fonctionne
- [ ] Génération PDF fonctionne
- [ ] PDF télécharge correctement
- [ ] Logs Vercel montrent les prints de debug
- [ ] Pas d'erreurs dans les logs

## 📊 Configuration Vercel

### vercel.json

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "50mb"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "/$1"
    }
  ],
  "functions": {
    "api/index.py": {
      "maxDuration": 60
    }
  }
}
```

### Points Importants

- **maxLambdaSize:** 50mb (pour ReportLab + Groq)
- **maxDuration:** 60s (pour génération IA)
- **Routes:** `/api/*` → Flask, `/*` → fichiers statiques

## 🎯 URLs de Production

- **Frontend :** https://synthesia-mu.vercel.app/
- **API Health :** https://synthesia-mu.vercel.app/api/health
- **API Generate :** https://synthesia-mu.vercel.app/api/generate-report

## 🔄 Rollback (si nécessaire)

```bash
# Revenir à un commit précédent
git log --oneline
git checkout <commit-hash>
git push origin main --force
```

## 📞 Support

En cas de problème :
1. Vérifier les logs Vercel
2. Tester `/api/health` en premier
3. Vérifier les variables d'environnement
4. Consulter la documentation Vercel Python

---

**✅ Structure optimale créée et prête pour production !**

