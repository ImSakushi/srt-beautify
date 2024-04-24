
# SRT Beautify

Ce projet offre une solution automatisée pour convertir les fichiers de sous-titres SRT en ASS, en appliquant un style spécifique (celui de Wakanim pour l'instant), et pour les fusionner avec des fichiers vidéo MKV/MP4. Le traitement peut être effectué via un script Python en ligne de commande ou une interface graphique utilisateur (GUI) basée sur Tkinter pour une interaction plus conviviale.

## Fonctionnalités

- **Conversion de SRT en ASS** : Convertit les fichiers de sous-titres SRT en format ASS avec un style prédéfini.
- **Fusion de sous-titres** : Ajoute la piste de sous-titres ASS modifiée aux fichiers vidéo MKV/MP4 en supprimant les pistes de sous-titres existantes.
- **Prise en charge multiple** : Traite plusieurs fichiers vidéo simultanément lors de l'utilisation de l'interface graphique.
- **Extraction automatique de sous-titres** : Pour les fichiers MKV, extrait automatiquement les sous-titres existants avant la conversion et la fusion.

## Prérequis

- Python 3.6 ou supérieur
- FFmpeg installé et accessible depuis le PATH de votre système
- Bibliothèques Python : `tkinter` pour l'interface graphique, `subprocess` pour l'exécution de commandes système

## Installation

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/ImSakushi/srt_beautify.git
   cd srt_beautify
   ```

2. **Installer FFmpeg** :
   - **Windows** : Téléchargez et installez depuis [FFmpeg.org](https://ffmpeg.org/download.html), et ajoutez le dossier `bin` à votre variable d'environnement PATH.
   - **Linux** : Exécutez `sudo apt-get install ffmpeg` (pour les distributions basées sur Debian).

3. **Assurez-vous que Python est installé** :
   - Vérifiez avec `python --version` ou `python3 --version`.

## Utilisation

### Script en Ligne de Commande

- Pour traiter une vidéo avec un fichier SRT spécifique :
  ```bash
  python srtass.py chemin/vers/la/video.mkv chemin/vers/le/sous-titre.srt
  ```

- Pour traiter une vidéo MKV en extrayant les sous-titres :
  ```bash
  python srtass.py chemin/vers/le/video.mkv
  ```

### Interface Graphique

- Lancez l'interface graphique :
  ```bash
  python gui.py
  ```

- Suivez les instructions à l'écran pour sélectionner les vidéos et le fichier SRT, puis cliquez sur "Process Videos" pour démarrer le traitement.
