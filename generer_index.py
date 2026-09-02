import os
import json
import re

def generer_liste_pdf():
    index_fichiers = {}
    # 1. On scanne tous les dossiers pour lister les PDF
    for root, dirs, files in os.walk("."):
        if ".git" in root or ".github" in root:
            continue
        
        pdf_trouves = [f for f in files if f.lower().endswith('.pdf')]
        if pdf_trouves:
            nom_dossier = os.path.basename(root)
            index_fichiers[nom_dossier] = sorted(pdf_trouves)
            
    # On écrit l'index dans le fichier JSON local
    with open("index_fichiers.json", "w", encoding="utf-8") as f:
        json.dump(index_fichiers, f, ensure_ascii=False, indent=4)
    print("✓ Fichier index_fichiers.json généré avec succès.")

    # 2. CHIRURGIE INVISIBLE SUR index.html
    # Le script va modifier uniquement la fonction fetch de l'API GitHub
    # sans jamais toucher au design, aux polices ou aux tableaux.
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            contenu = f.read()

        # On cherche l'appel à l'API GitHub dans votre JavaScript pour le rediriger vers le fichier local
        # Cette regex cible précisément l'URL de l'API sans impacter le reste du fichier HTML
        pattern_api = r"https://api\.github\.com/repos/had-lot/prepas/contents/[^\s'`\"]*"
        
        if re.search(pattern_api, contenu):
            # On remplace l'appel réseau par la lecture directe du fichier local
            nouveau_contenu = re.sub(pattern_api, "index_fichiers.json", contenu)
            
            with open("index.html", "w", encoding="utf-8") as f:
                f.write(nouveau_contenu)
            print("✓ Redirection réseau injectée de manière sécurisée dans index.html.")
        else:
            print("ℹ L'API GitHub n'a pas été détectée ou a déjà été patchée dans index.html.")

if __name__ == "__main__":
    generer_liste_pdf()
