#!/bin/bash

# ./install_venv.sh [cam]

# Le programme d'installation est appelé sans ou avec un argument,
# qui définit le type de caméra :
# - "opencv" pour les caméras USB,
# - "pi" pour la pi cam


WPATH=$(cd $(dirname $0) && pwd)    # répertoire de travail
DISTRIB=$(lsb_release -is)          # distribution linux

# Définit le fichier requirements pour l'installation
# des paquets python3 via pip3
if [ $# -lt 1 ]
then
    PIP_REQ="requirements.txt"
else
    PIP_REQ="requirements-$1.txt"
    
    if [ $1 = "opencv" ]
    then
	# Installation par gestionnaire de paquets d'opencv et numpy.
	# L'installation par pip3 ne fonctionne pas pour python 3.6-7.
	case $DISTRIB in
	    # VoidLinux : machine de test
	    "VoidLinux")
	    sudo xbps-install -S libopencv-python3
	    ;;
	"Debian" | "Raspbian")
	    sudo apt install python3-opencv -y
	    ;;
	esac
    fi
    case $DISTRIB in
        # VoidLinux : machine de test
        "VoidLinux")
        sudo xbps-install -S redis
        ;;
    "Debian" | "Raspbian")
        sudo apt install redis-server -y
        ;;
    esac
fi

echo $WPATH

# Installation de l'environnement virtuel
python3 -m venv $WPATH/env/

source $WPATH/env/bin/activate

PYTHON_VER="python3."$(python3 -c 'import sys; print(sys.version_info[1])')
echo $PYTHON_VER

pip3 install -r $PIP_REQ
deactivate

# Création des liens des librairies installées sur le système
# vers l'environnement virtuel pour opencv
if [ $# -eq 1 -a $1 == "opencv" ]
then
    CV2_LIB=$(python3 -c 'import cv2; print(cv2.__file__)')
    ln -s $CV2_LIB $WPATH/env/lib/$PYTHON_VER/site-packages/

    NUMPY_LIB=$(python3 -c 'import numpy; print(numpy.__path__)')
    NUMPY_LIB=${NUMPY_LIB%"']"}
    NUMPY_LIB=${NUMPY_LIB#"['"}
    ln -s $NUMPY_LIB $WPATH/env/lib/$PYTHON_VER/site-packages/
fi
