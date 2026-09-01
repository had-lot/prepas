import os
import json

def generer_liste_pdf():
    index_fichiers = {}
    # On parcourt tous les dossiers du site
    for root, dirs, files in os.walk("."):
        # On ignore les dossiers cachés du système
        if ".git" in root or ".github" in root:
            continue
        
        pdf_trouves = [f for f in files if f.lower().endswith('.pdf')]
        if pdf_trouves:
            # On utilise le nom du dossier comme catégorie
            nom_dossier = os.path.basename(root)
            index_fichiers[nom_dossier] = sorted(pdf_trouves)
            
    # On écrit le résultat dans un fichier de données indépendant
    with open("index_fichiers.json", "w", encoding="utf-8") as f:
        json.dump(index_fichiers, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    generer_liste_pdf()
