TimeLapse application
=====================
This project is another attempt to use the raspberry pi as a timelapse camera.
Goals
-----
- Control the timelapse remotely
- Allow streaming through web browser
- HTML interface
- Add functionnalities, even unused.(start, end, days of the week...)

References
----------
- On the streaming part
  - http://blog.miguelgrinberg.com/post/video-streaming-with-flask
  - http://blog.miguelgrinberg.com/post/flask-video-streaming-revisited.
- Hotspot configuration
  - http://www.raspberryconnect.com/projects/65-raspberrypi-hotspot-accesspoints/168-raspberry-pi-hotspot-access-point-dhcpcd-method
- Flask
  - https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

Manuel utilisateur
------------------
### Installation sur un Raspberry Pi vierge
* *Il est nécessaire d'être équipé d'un écran et d'un câble HDMI (ou d'un adapteur HDMI-VGA qui fonctionne).*
* *Le Raspberry doit être connecté au réseau pour que l'installation fonctionne.*

Alternativement, une installation peut être envisagé [en chroot depuis un système linux](https://gist.github.com/htruong/7df502fb60268eeee5bca21ef3e436eb)

1. Récupérer les codes sources du programme, par exemple sur github :
   `git clone https://github.com/PiZep/timelapse_control`
2. Dans le dossier se trouvent deux scripts d'installation :
  * `install_venv.sh`
  * `install_hotspot.sh`
   Le premier fichier permet d'installer les dépendences python, le second configure le Raspberry pi pour en faire un Hot Spot.
3. Le premier script s'utilise comme suit :
   <pre>./install_venv.sh <b>camera</b></pre>
   où `camera = pi` ou `opencv`. Si l'option est omise, `opencv` est le choix par défaut.
   *Exemple :*
   `./install_venv.sh pi`
4. Le second script requiert un numéro en paramètre, permettant d'identifier le Raspberry (dans le cas de l'utilisation de plusieurs appareils dans une même zone):
   <pre>./install_hotspot.sh <b>num</b></pre>
   *Exemple :*
   `./install_hotspot.sh 3`

**Les exemples suivant prennent les paramètres précédemment utilisés**

### Utilisation
Le Raspberry est accessible depuis tout appareil équipé du WiFi.

0. L'application est sensée se lancée automatiquement au démarrage. Cette partie n'a pas été intégrée, d'où la commande suivante.
   _Lancer l'application via :_ `./start_web_server.sh pi`

1. Se connecter au WiFi. Un serveur d'application Flask est lancé automatiquement au démarrage du Raspberry.

   *Nom du wifi :* `TimeLapse03`
2. Accéder à l'adresse IP du Raspberry dans un navigateur, sur le port 5000.

   *Adresse IP :* `http://192.168.3.10:5000`
3. La page qui s'ouvre (`/home`) montre la dernière capture réalisée et les paramètres du Time Lapse. Un clic sur le bouton `Configurer` permet d'accéder au flux vidéo et met en pause le Time Lapse.

![home capture](images/home.png?raw=true "/home page")

4. La page de configuration (`/config_timelapse`) permet de modifier les paramètres du Time Lapse. Les éléments importants sont :
  * Le switch pour mettre en route le Time Lapse, en haut à gauche,
  * L'intervalle entre deux prises de vue,
  * La résolution de la caméra (les options proposées sont compatibles avec la Pi Camera V2).
   Le bouton `Enregistrer` ramène à la page de présentation et **remet le TimeLapse en marche** (problème de threads actuellement, pas encore fonctionnel)

![config_timelapse capture](images/config_timelapse.png?raw=true "/config_timelapse page")

Des options supplémentaires sont accessibles si le Raspberry a accès à un seveur NTP, permettant de définir les plages horaires et les jours, notamment afin de limiter l'utilisation de la mémoire.

Organisation des fichiers source
--------------------------------
### Camera
* `stream_camera.py`
* `camera_opencv.py`
* `camera_pi.py`

Il s'agit des modules gérant la caméra, notamment la partie streaming (http://blog.miguelgrinberg.com/post/flask-video-streaming-revisited).
Le module stream_camera.py est la classe de base utilisé par les deux autres modules et n'est pas utilisée directement.
Ces modules permettent d'instancier une classe `Camera`

### Configuration
* `configmodule.py`
  Ce module gère la sérialisation des données, via la classe `ConfigJSON`.
* `configtl.py`, `configtl.json`
  Le module python définit la configuration de base et les règles de vérification. Le fichier json correspond à la sauvegarde réalisée durant le fonctionnement de l'application.

### Timelapse
* `timelapse.py`
Le module timelapse.py contient la logique du Time Lapse, via la classe `TimeLapse`, qui hérite de la clase `ConfigJSON`.
Cette dernière est instanciée avec en paramètre une classe `Camera` et un élément de configuration (un module, un nom de module, un dictionnaire...).

### Serveur Flask
* `server_app`.py
Le serveur Flask est le serveur d'application qui permet de générer l'interface utilisateur web. Tout est centralisé dans ce module.

### Autres
* `dotdict.py` : module permettant d'accéder aux clés des `dict` comme si elles étaient des attributs. Exemple : `d['key']` et `d.key` sont équivalents
* `templates` : contient les vues pour la génération des pages web
* `static` : fichiers statics, css et js
* `hotspot_scripts` : scripts et fichiers de configuration utilisés lors de l'installation du hotspot.
* `files.old` : anciens fichiers, utilisés lors du développement. Laissés à titre informatif, mais rien n'est trié.
* `webform.py` : tentative de clarification du code de `server_app.py`, pas encore aboutie.

TODO
----
* Faire en sorte que l'application démarre automatiquement, via `crontab` ou `systemd`.
* Intégrer un threading fonctionnel pour l'utilisation de la camera. Le streaming interrompt le time lapse si ce dernier survient pendant l'utilisation de la caméra.
* Clarifier le fichier `server_app.py` et réorganiser les méthodes et fonctions.
* Rendre l'interface plus cohérente. Le mélange de `bootstrap` et de css perso rend le tout assez laid.
