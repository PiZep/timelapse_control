#!/bin/bash

# ./install_venv.sh [cam]

# Le programme d'installation est appelé sans ou avec un argument,
# qui définit le type de caméra :
# - "opencv" pour les caméras USB,
# - "pi" pour la pi cam
# - rien ou "all" pour les deux.


WPATH=$(cd $(dirname $0) && pwd)    # répertoire de travail
DISTRIB=$(lsb_release -is)          # distribution linux

# Définit le fichier requirements pour l'installation
# des paquets python3 via pip3
if [ $# -lt 2 ]
then
	PIP_REQ="requirements.txt"
else
	PIP_REQ="requirements-$1.txt"
fi

echo $WPATH

# Installation par gestionnaire de paquets d'opencv et numpy.
# L'installation par pip3 ne fonctionne pas pour python 3.6-7.
case $DISTRIB in
    # VoidLinux : machine de test
	"VoidLinux")
		sudo xbps-install -s libopencv-python3
		;;
	"Debian" | "Raspbian")
		sudo apt install python3-opencv -y
		;;
esac

# Installation de l'environnement virtuel
python3 -m venv $WPATH/env/

pip3 install --user -r $PIP_REQ

# Création des liens des librairies installées sur le système
# vers l'environnement virtuel
PYTHON_VER="python3."&(python3 -c 'import sys; print(sys.version_info[1])')
ln -s /usr/lib/python3/dist-packages/{*cv2*,*numpy*} $WPATH/env/lib/$PYTHON_VER/site-packages/
