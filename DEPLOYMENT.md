# 🚀 Guide de Déploiement SyntheSIA sur Vercel

## ✅ Solution Implémentée : OPTION B - Routes API Vercel Natives

**Pourquoi cette solution ?**
- ✅ Format natif Vercel (pas de wrapper complexe)
- ✅ Chaque route = fichier Python séparé (plus maintenable)
- ✅ Pas de dépendance Flask (plus léger)
- ✅ Meilleure compatibilité avec le runtime Vercel
- ✅ Logs détaillés pour debug

## 📁 Structure des Fichiers

```
synthesia/
├── api/
│   ├── health.py              ← Route /api/health (GET)
│   ├── generate-report.py     ← Route /api/generate-report (POST)
│   └── utils/
│       ├── ai_handler.py      ← Client Groq (initialisé dans fonction)
│       └── pdf_generator.py   ← Génération PDF (utilise /tmp)
├── frontend/
│   └── index.html
├── vercel.json                ← Configuration Vercel
├── requirements.txt           ← Dépendances Python
└── .gitignore
```

## 🔧 Configuration Vercel

### 1. Variables d'Environnement Requises

Dans le dashboard Vercel → Settings → Environment Variables, ajouter :

```
GROQ_API_KEY = votre_clé_api_groq_ici
```

**⚠️ IMPORTANT :** Ne JAMAIS mettre la clé API dans le code source !

### 2. Configuration vercel.json

Le fichier `vercel.json` est déjà configuré avec :
- Build pour `api/health.py` et `api/generate-report.py`
- Routes pointant vers les bons fichiers
- maxLambdaSize: 15mb (pour ReportLab + Groq)

## 📝 Étapes de Déploiement

### Étape 1 : Vérifier les Fichiers

```bash
# Vérifier que tous les fichiers sont présents
ls api/health.py
ls api/generate-report.py
ls api/utils/ai_handler.py
ls api/utils/pdf_generator.py
ls vercel.json
ls requirements.txt
```

### Étape 2 : Vérifier les Variables d'Environnement

Dans Vercel Dashboard :
1. Aller dans Settings → Environment Variables
2. Vérifier que `GROQ_API_KEY` est définie
3. S'assurer qu'elle est disponible pour Production, Preview et Development

### Étape 3 : Déployer

```bash
# Si vous utilisez Vercel CLI
vercel --prod

# Ou pousser sur Git (si connecté à Vercel)
git add .
git commit -m "Migration vers handlers Vercel natifs"
git push origin main
```

### Étape 4 : Vérifier le Déploiement

1. **Test Health Check :**
   ```
   GET https://votre-projet.vercel.app/api/health
   ```
   Devrait retourner :
   ```json
   {
     "status": "online",
     "message": "SyntheSIA is running",
     "groq_configured": true,
     "environment": "production"
   }
   ```

2. **Test Génération PDF :**
   - Ouvrir https://votre-projet.vercel.app
   - Remplir le formulaire
   - Cliquer sur "Générer le rapport PDF"
   - Vérifier que le PDF se télécharge

## 🐛 Debug et Logs

### Voir les Logs Vercel

1. **Via Dashboard Vercel :**
   - Aller dans votre projet
   - Cliquer sur "Functions"
   - Sélectionner une fonction
   - Voir les logs en temps réel

2. **Via CLI :**
   ```bash
   vercel logs
   ```

### Logs Disponibles

Les handlers incluent des logs détaillés :
- ✅ Chargement des modules
- ✅ Appels de fonctions
- ✅ Erreurs avec traceback complet
- ✅ Informations de debug (méthode, path, headers)

### Erreurs Courantes

#### 1. "TypeError: issubclass() arg 1 must be a class"
**Cause :** Ancien handler Flask incompatible
**Solution :** Utiliser les nouveaux handlers natifs (déjà fait ✅)

#### 2. "ModuleNotFoundError: No module named 'utils'"
**Cause :** Chemin d'import incorrect
**Solution :** Les imports sont corrigés dans `generate-report.py` ✅

#### 3. "Permission denied: generated_reports/"
**Cause :** Vercel est read-only sauf /tmp
**Solution :** `pdf_generator.py` utilise maintenant `/tmp` ✅

#### 4. "GROQ_API_KEY not configured"
**Cause :** Variable d'environnement manquante
**Solution :** Ajouter `GROQ_API_KEY` dans Vercel Dashboard

#### 5. "Function timeout"
**Cause :** Génération IA trop longue
**Solution :** Vérifier les limites Vercel (Hobby = 10s, Pro = 60s)

## ✅ Checklist Post-Déploiement

- [ ] `/api/health` retourne `{"status": "online"}`
- [ ] `groq_configured: true` dans la réponse health
- [ ] `/api/generate-report` accepte POST avec JSON
- [ ] Le PDF se génère et se télécharge correctement
- [ ] Les logs Vercel montrent les prints de debug
- [ ] Pas d'erreurs dans les logs
- [ ] Le frontend appelle correctement les routes

## 🔄 Rollback (si nécessaire)

Si le déploiement échoue, vous pouvez :

1. **Revenir à l'ancien code :**
   ```bash
   git checkout HEAD~1 api/index.py
   git checkout HEAD~1 vercel.json
   ```

2. **Ou utiliser les anciens fichiers :**
   - `api/index.py` (ancien handler Flask)
   - Restaurer l'ancien `vercel.json`

## 📊 Monitoring

### Métriques à Surveiller

1. **Temps de réponse :**
   - `/api/health` : < 100ms
   - `/api/generate-report` : 5-15s (dépend de Groq)

2. **Taux d'erreur :**
   - Devrait être < 1%
   - Surveiller les erreurs 500

3. **Utilisation Lambda :**
   - Vérifier la taille des fonctions (< 15mb)
   - Surveiller les timeouts

## 🎯 URLs de Production

Après déploiement, vos URLs seront :
- **Frontend :** `https://votre-projet.vercel.app/`
- **Health :** `https://votre-projet.vercel.app/api/health`
- **Generate :** `https://votre-projet.vercel.app/api/generate-report`

## 📞 Support

En cas de problème :
1. Vérifier les logs Vercel
2. Tester `/api/health` en premier
3. Vérifier les variables d'environnement
4. Consulter la documentation Vercel Python

---

**Dernière mise à jour :** Migration vers handlers Vercel natifs (Option B)
**Statut :** ✅ Prêt pour production

