# 🔧 Guide de Test - Toutes les Solutions

## Problème Actuel
- Frontend 404 sur https://synthesia-mu.vercel.app/
- API crash 500 sur /api/health

## Solutions Créées

### Solution 1 : Handlers Natifs Simplifiés (ACTUELLE)
**Fichiers :**
- `api/health.py` - handler natif simplifié
- `api/generate-report.py` - handler natif simplifié
- `vercel.json` - configuration actuelle

**Test :**
```bash
git add .
git commit -m "solution 1: handlers natifs simplifiés"
git push origin main
```

**Vérifier :**
- https://synthesia-mu.vercel.app/api/health
- https://synthesia-mu.vercel.app/

---

### Solution 2 : Flask avec api/index.py
**Fichiers :**
- `api/index.py` - app flask complète
- `vercel-flask.json` - configuration flask

**Activer :**
```bash
# renommer vercel.json en vercel-old.json
mv vercel.json vercel-old.json

# utiliser la config flask
mv vercel-flask.json vercel.json

# ajouter flask dans requirements.txt si pas présent
echo "flask==3.0.0" >> requirements.txt
echo "flask-cors==4.0.0" >> requirements.txt

git add .
git commit -m "solution 2: flask avec index.py"
git push origin main
```

**Vérifier :**
- https://synthesia-mu.vercel.app/api/health
- https://synthesia-mu.vercel.app/

---

### Solution 3 : Test Ultra Simple
**Fichier :**
- `api/test-simple.py` - handler minimal

**Tester :**
1. Modifier `vercel.json` :
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/test-simple.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/test",
      "dest": "api/test-simple.py"
    }
  ]
}
```

2. Tester : https://synthesia-mu.vercel.app/api/test

Si ça marche, le problème vient du format des handlers.

---

## Checklist Debug

### 1. Vérifier les Logs Vercel
- Dashboard Vercel → Project → Functions → Logs
- Chercher les erreurs Python
- Vérifier les prints de debug

### 2. Vérifier les Variables d'Environnement
- Dashboard Vercel → Settings → Environment Variables
- `GROQ_API_KEY` doit être définie
- Disponible pour Production, Preview, Development

### 3. Vérifier la Structure
```
synthesia/
├── api/
│   ├── health.py          ✅
│   ├── generate-report.py ✅
│   ├── index.py          ✅ (flask)
│   ├── test-simple.py    ✅ (test)
│   └── utils/
│       ├── ai_handler.py ✅
│       └── pdf_generator.py ✅
├── public/
│   └── index.html        ✅
├── vercel.json           ✅
├── requirements.txt       ✅
└── .gitignore            ✅
```

### 4. Tester Localement (Optionnel)
```bash
# installer vercel cli
npm install -g vercel

# tester local
vercel dev
```

---

## Ordre de Test Recommandé

1. **Solution 1** (handlers natifs simplifiés) - ACTUELLE
   - Déjà déployée
   - Vérifier les logs

2. **Solution 2** (Flask) - Si Solution 1 ne marche pas
   - Plus compatible avec Vercel
   - Meilleur support

3. **Solution 3** (test simple) - Pour diagnostiquer
   - Vérifier que Vercel fonctionne
   - Isoler le problème

---

## Erreurs Courantes et Solutions

### "ModuleNotFoundError"
- Vérifier que tous les imports sont corrects
- Vérifier que `sys.path` est configuré

### "Permission denied"
- Utiliser `/tmp` pour les fichiers temporaires
- Vérifier que `pdf_generator.py` utilise `/tmp`

### "TypeError: handler()"
- Vérifier le format du handler
- Tester avec `test-simple.py` d'abord

### "404 NOT_FOUND"
- Vérifier `vercel.json` routes
- Vérifier que `public/index.html` existe
- Vérifier que les builds sont configurés

---

## Commandes Git Rapides

```bash
# solution 1 (actuelle)
git add api/health.py api/generate-report.py vercel.json
git commit -m "solution 1: handlers simplifiés"
git push

# solution 2 (flask)
git add api/index.py vercel-flask.json requirements.txt
mv vercel.json vercel-old.json
mv vercel-flask.json vercel.json
git add vercel.json
git commit -m "solution 2: flask"
git push

# revenir à solution 1
git checkout HEAD~1 -- vercel.json
git add vercel.json
git commit -m "retour solution 1"
git push
```

---

**Dernière mise à jour :** Toutes les solutions créées et prêtes à tester

