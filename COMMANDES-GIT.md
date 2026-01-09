# 📋 Commandes Git Exactes pour Déploiement

## ✅ Étape 1 : Vérifier les Changements

```bash
git status
```

Vous devriez voir :
- `api/health.py` (nouveau)
- `api/generate-report.py` (nouveau)
- `api/utils/pdf_generator.py` (modifié)
- `vercel.json` (modifié)
- `requirements.txt` (modifié)
- `DEPLOYMENT.md` (nouveau)
- `CHANGELOG.md` (nouveau)
- `COMMANDES-GIT.md` (nouveau)
- `verify-deployment.sh` (nouveau)

## ✅ Étape 2 : Ajouter les Fichiers

```bash
git add api/health.py
git add api/generate-report.py
git add api/utils/pdf_generator.py
git add vercel.json
git add requirements.txt
git add DEPLOYMENT.md
git add CHANGELOG.md
git add COMMANDES-GIT.md
git add verify-deployment.sh
```

**OU en une seule commande :**

```bash
git add api/health.py api/generate-report.py api/utils/pdf_generator.py vercel.json requirements.txt DEPLOYMENT.md CHANGELOG.md COMMANDES-GIT.md verify-deployment.sh
```

## ✅ Étape 3 : Commit

```bash
git commit -m "Migration vers handlers Vercel natifs (Option B)

- Création api/health.py et api/generate-report.py (handlers natifs)
- Modification pdf_generator.py pour utiliser /tmp (Vercel read-only)
- Mise à jour vercel.json avec nouvelles routes
- Nettoyage requirements.txt (suppression Flask)
- Ajout documentation déploiement et changelog
- Correction bug 'TypeError: issubclass() arg 1 must be a class'
- Support complet CORS et gestion d'erreurs
- Logs détaillés pour debug"
```

## ✅ Étape 4 : Push vers GitHub

```bash
git push origin main
```

**OU si votre branche principale s'appelle `master` :**

```bash
git push origin master
```

## ✅ Étape 5 : Vérifier le Déploiement Vercel

1. **Attendre le build Vercel** (2-5 minutes)
   - Vérifier dans Vercel Dashboard → Deployments

2. **Tester l'endpoint health :**
   ```bash
   curl https://votre-projet.vercel.app/api/health
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

3. **Vérifier les logs Vercel :**
   - Dashboard Vercel → Functions → health.py
   - Vérifier qu'il n'y a pas d'erreurs

## 🔄 Si le Déploiement Échoue

### Option 1 : Rollback Rapide

```bash
git revert HEAD
git push origin main
```

### Option 2 : Revenir à l'Ancien Code

```bash
git checkout HEAD~1 -- api/index.py vercel.json
git commit -m "Rollback vers ancien handler Flask"
git push origin main
```

## 📝 Checklist Avant de Push

- [ ] Tous les fichiers sont ajoutés (`git status` propre)
- [ ] Variable `GROQ_API_KEY` définie dans Vercel Dashboard
- [ ] Aucune clé API dans le code source
- [ ] `vercel.json` est valide JSON
- [ ] `requirements.txt` contient toutes les dépendances
- [ ] Les imports Python sont corrects
- [ ] Le frontend appelle `/api/generate-report` (déjà fait ✅)

## 🎯 Après le Push

1. **Surveiller les logs Vercel** pendant le build
2. **Tester `/api/health`** dès que le déploiement est terminé
3. **Tester la génération PDF** via le frontend
4. **Vérifier qu'il n'y a pas d'erreurs** dans les logs

---

**Note :** Si vous utilisez Vercel CLI, vous pouvez aussi déployer avec :
```bash
vercel --prod
```

Mais le push Git est recommandé pour garder un historique propre.

