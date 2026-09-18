// chargeur.js
// Remplace la fonction chargerDossier d'index.html
// pour lire les données locales (data.js) au lieu de l'API GitHub.

(function () {

  function getIndex() {
    // On lit INDEX_PDF au moment de l'appel, pas au chargement.
    return window.INDEX_PDF || window.DATA_PDF || window.data || window.cours || {};
  }

  function normaliserChemin(chemin) {
    return (chemin || "").replace(/^\.\//, "").replace(/\/+$/, "").trim();
  }

  function listerContenu(chemin) {
    const INDEX = getIndex();
    const cheminNorm = normaliserChemin(chemin);

    const sousDossiers = [];
    const fichiers = [];

    // 1) Correspondance exacte
    for (const cle in INDEX) {
      const cleNorm = normaliserChemin(cle);
      if (cleNorm === cheminNorm) {
        for (const f of INDEX[cle]) {
          if (f.toLowerCase().endsWith(".pdf")) fichiers.push(f);
        }
      }
    }

    // 2) Sous-dossiers
    const prefixe = cheminNorm + "/";
    for (const cle in INDEX) {
      const cleNorm = normaliserChemin(cle);
      if (cleNorm.startsWith(prefixe)) {
        const reste = cleNorm.slice(prefixe.length);
        const premierSegment = reste.split("/")[0];
        if (premierSegment && !sousDossiers.includes(premierSegment)) {
          sousDossiers.push(premierSegment);
        }
      }
    }

    return { sousDossiers, fichiers };
  }

  window.chargerDossier = function (containerId, path) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const { sousDossiers, fichiers } = listerContenu(path);

    if (sousDossiers.length === 0 && fichiers.length === 0) {
      container.innerHTML = "<div class='file-list'>📭 Aucun fichier</div>";
      return;
    }

    let html = "";

    // Sous-dossiers cliquables
    for (const dossier of sousDossiers) {
      const subId = containerId + "_" + dossier.replace(/[^a-z0-9]/gi, "_");
      html += `<div class="folder-item"><div class="folder-title" onclick="event.stopPropagation(); toggleFolder(this)">${dossier}</div><div id="${subId}" class="folder-content" data-path="${path}/${dossier}"></div></div>`;
    }

    // Fichiers PDF
    if (fichiers.length) {
      html += "<div class='file-list'><ul>";
      for (const f of fichiers) {
        const encodedPath = path.split("/").map(encodeURIComponent).join("/");
        const rawUrl = `https://media.githubusercontent.com/media/had-lot/prepas/main/${encodedPath}/${encodeURIComponent(f)}`;
        html += `<li>📄 <a href="${rawUrl}" target="_blank" style="color:#2a5298; text-decoration:none;">${f.replace(/\.pdf$/i, "")}</a></li>`;
      }
      html += "</ul></div>";
    }

    container.innerHTML = html;
  };

  // Si data.js arrive APRÈS chargeur.js, on recharge la page une fois.
  // Ceinture et bretelles.
  window.addEventListener("load", function () {
    if (!window.INDEX_PDF && !window.DATA_PDF && !window.data && !window.cours) {
      console.warn("⚠️ data.js pas encore chargé — attente…");
    }
  });
})();
