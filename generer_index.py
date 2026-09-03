import os
import json
import re
import sys

def generer_liste_pdf():
    index_fichiers = {}
    
    print("🔍 Scan des dossiers en cours...")
    
    # 1. On scanne tous les dossiers pour lister les PDF
    for root, dirs, files in os.walk("."):
        # Ignorer les dossiers cachés et systèmes
        if any(ignored in root for ignored in [".git", ".github", "__pycache__", ".venv"]):
            continue
        
        pdf_trouves = [f for f in files if f.lower().endswith('.pdf')]
        if pdf_trouves:
            # Utiliser le nom du dossier parent pour une meilleure organisation
            nom_dossier = os.path.basename(root)
            if nom_dossier == ".":
                nom_dossier = "racine"
            
            # Ajouter le chemin relatif pour plus de clarté
            chemin_relatif = os.path.relpath(root, ".")
            if chemin_relatif != ".":
                nom_affichage = f"{nom_dossier} ({chemin_relatif})"
            else:
                nom_affichage = nom_dossier
            
            index_fichiers[nom_affichage] = sorted(pdf_trouves)
            print(f"  📁 {nom_affichage}: {len(pdf_trouves)} PDF trouvés")
    
    # 2. On écrit l'index dans le fichier JSON local
    try:
        with open("index_fichiers.json", "w", encoding="utf-8") as f:
            json.dump(index_fichiers, f, ensure_ascii=False, indent=4)
        print(f"✅ Fichier index_fichiers.json généré avec succès ({sum(len(v) for v in index_fichiers.values())} PDF au total).")
    except Exception as e:
        print(f"❌ Erreur lors de l'écriture du fichier JSON : {e}")
        return False

    # 3. Patch automatique de index.html (optionnel mais utile)
    if os.path.exists("index.html"):
        try:
            with open("index.html", "r", encoding="utf-8") as f:
                contenu = f.read()
            
            # Vérifier si le fichier utilise déjà l'API GitHub
            pattern_api = r"https://api\.github\.com/repos/had-lot/prepas/contents/[^\s'`\"]*"
            
            if re.search(pattern_api, contenu):
                nouveau_contenu = re.sub(pattern_api, "index_fichiers.json", contenu)
                
                with open("index.html", "w", encoding="utf-8") as f:
                    f.write(nouveau_contenu)
                print("✅ Redirection réseau injectée dans index.html.")
            else:
                # Vérifier si la redirection est déjà en place
                if 'index_fichiers.json' in contenu:
                    print("ℹ La redirection est déjà en place dans index.html.")
                else:
                    print("⚠️ Aucun appel API GitHub trouvé. Vérifiez que votre index.html utilise l'URL correcte.")
        except Exception as e:
            print(f"⚠️ Erreur lors de la modification de index.html : {e}")
    else:
        print("ℹ index.html non trouvé (peut-être dans un autre dossier)")

    return True

if __name__ == "__main__":
    success = generer_liste_pdf()
    sys.exit(0 if success else 1)
