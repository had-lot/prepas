import os
import json

def generer_liste_pdf():
    index_fichiers = {}
    index_fichiers_avec_point = {} # Pour compatibilité avec les chemins du style "./MPSI"
    
    print("🔍 Scan des dossiers en cours...")
    
    for root, dirs, files in os.walk("."):
        if ".git" in root or ".github" in root or "__pycache__" in root:
            continue
        
        pdf_trouves = [f for f in files if f.lower().endswith('.pdf')]
        if pdf_trouves:
            chemin_relatif = os.path.relpath(root, ".")
            if chemin_relatif == ".":
                nom_dossier = "Racine"
                nom_dossier_point = "Racine"
            else:
                nom_dossier = chemin_relatif.replace(os.sep, "/")
                nom_dossier_point = f"./{nom_dossier}"
            
            pdf_tries = sorted(pdf_trouves)
            index_fichiers[nom_dossier] = pdf_tries
            index_fichiers_avec_point[nom_dossier_point] = pdf_tries
            print(f"  📁 {nom_dossier}: {len(pdf_trouves)} PDF")
    
    # 1. Écriture du JSON classique
    with open("index_fichiers.json", "w", encoding="utf-8") as f:
        json.dump(index_fichiers, f, ensure_ascii=False, indent=4)
        
    # NOUVEAU : On génère aussi un fichier nommé index.json au cas où le HTML chercherait ce nom standard
    with open("index.json", "w", encoding="utf-8") as f:
        json.dump(index_fichiers, f, ensure_ascii=False, indent=4)
    
    # 2. Écriture du fichier data.js super-compatible
    with open("data.js", "w", encoding="utf-8") as f:
        # On écrit la variable que vous aviez
        f.write("window.INDEX_PDF = ")
        json.dump(index_fichiers, f, ensure_ascii=False, indent=2)
        f.write(";\n")
        
        # NOUVEAU : On ajoute les variantes avec "./" au cas où le HTML en aurait besoin
        f.write("window.INDEX_PDF_ALT = ")
        json.dump(index_fichiers_avec_point, f, ensure_ascii=False, indent=2)
        f.write(";\n")
        
        # NOUVEAU : On injecte aussi dans d'autres noms de variables très courants
        f.write("window.data = window.INDEX_PDF;\n")
        f.write("window.DATA_PDF = window.INDEX_PDF;\n")
        f.write("window.cours = window.INDEX_PDF;\n")
    
    total_pdfs = sum(len(v) for v in index_fichiers.values())
    print(f"✅ Index universel généré avec succès !")
    print(f"📄 Fichiers mis à disposition de index.html : index_fichiers.json, index.json et data.js")

if __name__ == "__main__":
    generer_liste_pdf()
