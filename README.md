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
