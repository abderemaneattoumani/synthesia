@echo off
echo ==========================================
echo  VERIFICATION SECURITE AVANT PUSH
echo ==========================================
echo.

echo [1/3] Verification fichier .env...
git ls-files | findstr /i "\.env$"
if %ERRORLEVEL% EQU 0 (
    echo [ERREUR] Le fichier .env est tracke par Git !
    echo Action requise : git rm --cached backend/.env
    exit /b 1
) else (
    echo [OK] Fichier .env ignore correctement
)
echo.

echo [2/3] Recherche de cles API dans les fichiers commites...
git grep -i "gsk_" > nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [ERREUR] Cle API detectee dans le code !
    echo Fichiers concernes :
    git grep -i "gsk_"
    exit /b 1
) else (
    echo [OK] Aucune cle API detectee
)
echo.

echo [3/3] Verification .gitignore...
if exist .gitignore (
    findstr /i ".env" .gitignore > nul
    if %ERRORLEVEL% EQU 0 (
        echo [OK] .gitignore contient .env
    ) else (
        echo [AVERTISSEMENT] .env absent du .gitignore
    )
) else (
    echo [ERREUR] Fichier .gitignore manquant !
    exit /b 1
)
echo.

echo ==========================================
echo  VERIFICATION TERMINEE - TOUT EST OK !
echo ==========================================
echo Vous pouvez faire git push en securite.
pause