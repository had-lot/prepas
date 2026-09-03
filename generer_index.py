import os
import json

def generer_liste_pdf():
    index_fichiers = {}
    
    print("🔍 Scan des dossiers en cours...")
    
    # 1. On scanne tous les dossiers pour lister les PDF
    for root, dirs, files in os.walk("."):
        if ".git" in root or ".github" in root or "__pycache__" in root:
            continue
        
        pdf_trouves = [f for f in files if f.lower().endswith('.pdf')]
        if pdf_trouves:
            # Utiliser le chemin relatif comme clé
            chemin_relatif = os.path.relpath(root, ".")
            if chemin_relatif == ".":
                nom_dossier = "Racine"
            else:
                nom_dossier = chemin_relatif.replace(os.sep, "/")
            
            index_fichiers[nom_dossier] = sorted(pdf_trouves)
            print(f"  📁 {nom_dossier}: {len(pdf_trouves)} PDF")
    
    # 2. On écrit uniquement l'index dans le fichier JSON
    with open("index_fichiers.json", "w", encoding="utf-8") as f:
        json.dump(index_fichiers, f, ensure_ascii=False, indent=4)
    
    total_pdfs = sum(len(v) for v in index_fichiers.values())
    print(f"✅ Index généré avec {len(index_fichiers)} dossiers et {total_pdfs} PDF")
    print(f"📄 Fichier: index_fichiers.json")

if __name__ == "__main__":
    generer_liste_pdf()
