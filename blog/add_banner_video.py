#!/usr/bin/env python3
"""Ajoute la vidéo thématique (comme sur les pages services) dans le bandeau de chaque article du blog."""
import os
import re

BLOG_DIR = os.path.dirname(os.path.abspath(__file__))

# Vidéos disponibles sur les pages services (chemins depuis blog/ = ../assets/...)
VIDEOS = {
    "panneaux": "../assets/panneausolairegreensolar.mp4",
    "batterie": "../assets/batteriestockage.mp4",
    "carport": "../assets/carportpv.mp4",
    "borne": "../assets/bornederechargevideogreensolar.mp4",
    "clotures": "../assets/videocloturepv.mp4",
    "domotique": "../assets/domotiquevideo.mp4",
    "maintenance": "../assets/savgreensolar.mp4",
}

def video_for_file(filename):
    """Choisit la vidéo la plus en thème selon le nom du fichier."""
    name = filename.lower()
    if "batterie-stockage" in name or "batterie" in name:
        return VIDEOS["batterie"]
    if "borne-recharge" in name or "borne" in name and "recharge" in name:
        return VIDEOS["borne"]
    if "carport" in name:
        return VIDEOS["carport"]
    if "cloture" in name or "clôture" in name:
        return VIDEOS["clotures"]
    if "domotique" in name:
        return VIDEOS["domotique"]
    if "maintenance" in name and "panneaux" in name:
        return VIDEOS["maintenance"]
    # Par défaut : panneaux / solaire général
    return VIDEOS["panneaux"]

def process_file(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    # Déjà une vidéo dans le bandeau ?
    if "breadcum-video-bg" in content and "breadcum" in content:
        # Vérifier que c'est bien dans la section breadcum
        if re.search(r'<section class="breadcum[^"]*"[^>]*>\s*<video', content):
            return False, "video déjà présente"
    # Pattern: <section class="breadcum ..."> éventuellement \n ou espaces <div class="container">
    pattern = r'(<section class="breadcum bg-cover-center v1 py-50 py-sm-80 py-md-120">)\s*(<div class="container">)'
    video_src = video_for_file(os.path.basename(path))
    replacement = r'\1<video autoplay class="breadcum-video-bg" loop muted playsinline><source src="' + video_src + r'" type="video/mp4"/></video>\2'
    if not re.search(pattern, content):
        return False, "pattern breadcum non trouvé"
    new_content = re.sub(pattern, replacement, content, count=1)
    if new_content == content:
        return False, "aucun remplacement"
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    return True, os.path.basename(path).replace(".html", "")

def main():
    updated = 0
    for name in sorted(os.listdir(BLOG_DIR)):
        if name == "index.html" or not name.endswith(".html"):
            continue
        path = os.path.join(BLOG_DIR, name)
        if not os.path.isfile(path):
            continue
        ok, msg = process_file(path)
        if ok:
            updated += 1
            print(f"OK {name} → {msg}")
        else:
            if "déjà" in msg or "pattern" in msg:
                print(f"SKIP {name}: {msg}")
    print(f"\n{updated} fichier(s) mis à jour.")

if __name__ == "__main__":
    main()
