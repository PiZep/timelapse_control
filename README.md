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

Manuel d'utilisation
--------------------
### Le programme visé
#### Installation sur un Raspberry Pi vierge
* **Il est nécessaire d'être équipé d'un écran et d'un câble HDMI (ou d'un adapteur HDMI-VGA qui fonctionne).**
* **Le Raspberry doit être connecté au réseau pour que l'installation fonctionne.**
Une installation peut être envisagé en chroot depuis un système linux :
`https://gist.github.com/htruong/7df502fb60268eeee5bca21ef3e436eb`
1. Récupérer les sources du programme sur github :
   `git clone https://github.com/PiZep/timelapse_control`
2. Dans le dossier se trouvent deux scripts d'installation :
  * `install_venv.sh`
  * `install_hotspot.sh`
   Le premier fichier permet d'installer les dépendences python, le second configure le Raspberry pi pour en faire un Hot Spot.
3. Le premier script s'utilise comme suit :
   <pre>./install_venv.sh <b>camera</b></pre>
   ou `camera = pi` ou `opencv`. Si l'option est omise, `opencv` est le choix par défaut.
4. Le second script requiert un numéro en paramètre, permettant de l'identifier de manière unique :
   <pre>./install_hotspot.sh <b>num</b></pre>

#### Utilisation
1. Se connecter au WiFi
