import os
import json
import re
from urllib.parse import quote

def generer_liste_pdf():
    index_fichiers = {}
    
    print("🔍 Scan des dossiers en cours...")
    
    # 1. On scanne tous les dossiers pour lister les PDF
    for root, dirs, files in os.walk("."):
        # Ignorer les dossiers système
        if any(ignored in root for ignored in [".git", ".github", "__pycache__"]):
            continue
        
        pdf_trouves = [f for f in files if f.lower().endswith('.pdf')]
        if pdf_trouves:
            # Nettoyer le chemin pour l'affichage
            chemin_relatif = os.path.relpath(root, ".")
            if chemin_relatif == ".":
                nom_affichage = "Racine"
            else:
                # Remplacer les backslashes par des slashes pour l'URL
                nom_affichage = chemin_relatif.replace(os.sep, "/")
            
            # Stocker les fichiers triés
            index_fichiers[nom_affichage] = sorted(pdf_trouves)
            print(f"  📁 {nom_affichage}: {len(pdf_trouves)} PDF")
    
    # 2. Écrire l'index dans le fichier JSON
    with open("index_fichiers.json", "w", encoding="utf-8") as f:
        json.dump(index_fichiers, f, ensure_ascii=False, indent=4)
    
    total_pdfs = sum(len(v) for v in index_fichiers.values())
    print(f"✅ Index généré avec {len(index_fichiers)} dossiers et {total_pdfs} PDF")
    return index_fichiers

if __name__ == "__main__":
    generer_liste_pdf()
