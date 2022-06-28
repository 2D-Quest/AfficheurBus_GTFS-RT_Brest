# AfficheurBus_GTFS-RT_Brest

## Introduction
Cette documentation s’adresse à toute personne souhaitant créer un afficheur des temps d’arrivées des bus de la compagnie Bibus, similaire à ce qu’on peut trouver au niveau des arrêts de bus.
Cet afficheur affichera les temps d’arrivées des bus à l’arrêt bouguen en face de l’UFR Sciences et Techniques de Brest.

Pour réaliser cet afficheur, il faut utiliser les informations proposées par le site data.gouv.fr, qui met à disposition des données concernant les transports en commun de différentes villes en France. Les données qui nous intéressent sont récupérées à l’aide de fichiers au format GTFS-RT et GTFS

Un minimum de connaissances en informatique et en utilisation de Raspberry Pi sont requises pour réaliser l’afficheur. 
Le langage utilisé pour le programme récupérant les données, est le Python.

## Liste du Matériel électronique

-Raspberry Pi 3 Model B V1.2
-Cable d’alimentation pour la raspberry, un USB-MicroUSB 
-Carte SD de minimum 8Go
-I2C 16x2 Arduino LCD Display Module 
-Fils de câblages

## Liste des Ressources Informatiques

-Logiciel Raspberry Pi Imager (https://www.raspberrypi.com/software/)
-Module GTFS-Realtime (https://pypi.org/project/gtfs-realtime-bindings/)
-Module urllib.request (https://docs.python.org/fr/3/library/urllib.html)
-Module 
-Bibliothèque LCD de the-raspberry-pi-guy (https://www.giters.com/the-raspberry-pi-guy/lcd)
-Bibliothèque CSV pour python (https://docs.python.org/fr/3/library/csv.html)

## Fichiers sources

## Schéma de parcours des données

## Architecture électronique

## Algorithme du Programme

## Tutoriel pour la programmation

1ère étape : Installer, à l’aide de la carte SD et du logiciel Raspberry Pi Imager, le Raspberry Pi OS sur votre Raspberry PI 3, prendre la version 64-Bit et de préférence une version plus légère.

2éme étape: Insérer la carte SD dans la Raspberry, brancher un clavier et une souris et suivez les étapes indiquées sur l’écran. 

3éme étape: Dans le terminal Linux (Ctrl+Alt+T) taper les commandes suivantes:
    pip install gtfs-realtime-bindings
    sudo apt install git
    cd /home/pi/
    git clone https://github.com/the-raspberry-pi-guy/lcd.git
    cd lcd/
    sudo ./install.sh

4éme étape: Une fois la configuration initiale terminée en appuyant sur la touche démarrer un menu déroulant apparaîtra et un onglet programmation sera présent, chercher Thony IDE et lancez l’application, récupérer le fichiers source dans son intégralité et ouvrez le fichiers gtfs_bibus.py dans Thony Ide.

Une fois ces étapes terminées, le programme devrait afficher le temps d'arrivée du prochain bus et sa direction, pour les 3 arrêts bouguen en face de l’UFR Sciences et Techniques de Brest, pour plus de détails et de personnalisation du programme suivre les sections suivantes.

## Utilisation du format GTFS-RT et GTFS avec une Raspberry Pi 3

Nouveau format de partage de données en temps réel des transports en commun, le GTFS-RT s'appuie nécessairement sur un fichier GTFS décrivant les lignes et horaires théoriques, car il indique la différence observée par rapport à ces horaires prévus.

Ainsi nous allons voir dans cette section comment utiliser ces deux formats de données, pour l’afficheur de temps d'arrivée.

1ère étape:Configuration du programme:
Importer toutes les bibliothèques et modules nécessaires à l'exécution du programme indiquez plus haut et dans le code source.
La plus importante et non remplaçable étant le: from google.transit import gtfs_realtime_pb2 as gtfs ,installé au préalable dans la section précédente, permettant la manipulation de fichiers GTFS.
Définition, des arrêts dont on veut le temps d’arrivées des Bus dans le tableaux arrêt et définition du temps limite dans la variable limite, qui va définir le maximum du temps d’arrivées afficher pour un bus. Pour connaître la nomenclature d’un arrêt sous le format GTFS la liste des arrêts est disponible dans le fichiers GTFS,si on souhaite les temps d’arrivées de bus de l’arrêt Liberté on mettre dans la liste arret  “OCTROI_1” et “OCTROI_2” pour avoir les deux stations de bus nommer Octroi et pour les trams ”OCTRO_TA” et “OCTRO_TR”. Il est possible de vérifier que l’arrêt choisi avec les coordonnées fournit par le GTFS.

Récupération des lien/fichiers GTFS-RT et GTFS:
1)Récupération du fichier GTFS, décrivant les lignes et horaires théorique du réseaux Bibus, disponible à ce lien : https://www.data.gouv.fr/fr/datasets/r/583d1419-058b-481b-b378-449cab744c82, dans le dossier télécharger renommer les fichiers trips.txt et stops.txt en trips.csv et stops.csv qui seront stocker dans les variables trip_meta et stop_meta. 

2) récupération de l’url permettant la récupération dynamique du fichiers GTFS-RT, qui est la suivante :https://www.data.gouv.fr/fr/datasets/r/f7cbc4f8-da19-4bf3-8c88-c4afda0090a4
que l’on va stocker dans la variable du code source url_data_bibus

2éme étape :  Fonction de récupération et d’organisation des temps d’arrivées des bus:
Dans le fichiers GTFS-RT trip_update les données sont organisées en différentes classes et sous-classes, les temps d’arrivés des bus sont contenus dans la clause stop_time_update contenu elle même dans la sous classe trip_update contenu dans la classe entity du fichiers trip_update. Avec des boucles for il faut parcourir ces classes (voir code source) et quand un stop_id (id des arrêt de bus) correspond à un des arrêt qui nous intéresse (défini dans la liste arret) il est ajouter dans notre dictionnaire MAJ_horaire.

3éme étape : Fonction d’affichage des temps d’arrivées des bus sur le terminal Thony IDE et sur l’écran LCD:
A chaque appel de cette fonction on initialisera l’écran LCD pour éviter un bug (sleep) en utilisant la bibliothèque précédemment installer drivers, on va ensuite définir plusieurs variables pour nous permettre de calculer le temps de trajet et donc afficher les bonnes informations sur l’écran LCD.
On va ensuite vérifier si le temps en minute d'arrivée est inférieur ou égale à 1 , si le temps est inférieur à 1 on affichera "Arrivée imminente", sinon on affichera le temps en minutes.

4eme étape: Programme principale main:
Créer les dictionnaires qui contiennent les informations des trajets et des arrêts sous un format csv
Entrée dans une boucle infinie qui appelle va d’abord appeler la fonction obtenirMAJ est stockage du résultat dans le dictionnaire updates. Ensuite l’affichage se fera à l’aide d’une boucle for qui va appeler pour chaque élément du dictionnaire la fonction d’affichage.
L’affichage se fera du bus arrivant le plus tôt à celui arrivant le plus tard.

## Paramétrages de la raspberry pour que le programme se lance à la mise sous tension.

Pour simplifier l’utilisation de l’afficheur il est possible de lancer le programme sans utiliser d’écran de clavier ou de souris.
Pour cela:
-Se connecter au wifi au moins une fois avant de déployer l’objet connecté, 
-Créer un script shell qui sera éxécuter tout seul au lancement de la raspberry (tutoriel en françaishttps://www.raspberrypi-france.fr/lancer-un-script-python-au-demarrage-du-raspberry-pi/ )
-Le script est disponible dans les fichiers source (lancement.sh) il est important de rajouter dans le crontab la commande sudo.

## Webographie

https://www.data.gouv.fr/fr/datasets/r/f7cbc4f8-da19-4bf3-8c88-c4afda0090a4 (GTFS dynamique url stable)
https://proxy.transport.data.gouv.fr/resource/bibus-brest-gtfs-rt-trip-update 
https://www.data.gouv.fr/fr/datasets/r/583d1419-058b-481b-b378-449cab744c82 (GTFS Statique)
https://www.data.gouv.fr/fr/datasets/horaires-theoriques-et-temps-reel-des-bus-et-tramways-circulant-sur-le-territoire-de-brest-metropole/ (jeux de données data.gouv.fr pour bibus)

http://gtfsbook.com/gtfs-realtime-book-sample.pdf (explication GTFS)

https://docs.python.org/fr/3/library/urllib.html (doc urlib)

https://developers.google.com/transit/gtfs-realtime/reference (schéma classe GTFS-RT)

-https://developers.google.com/protocol-buffers/docs/reference/python-generated#singular-fields-proto3

https://developers.google.com/transit/gtfs-realtime/examples/python-sample?hl=fr


- https://developers.google.com/transit/gtfs-realtime/reference

https://api.gouv.fr/documentation/temps_reel_transport 

https://developers.google.com/transit/gtfs-realtime/examples/python-sample?hl=fr (installation BIBLIOTHEQUE GTFS)


https://github.com/etalab/transpo-rt (documentation github)

https://github.com/boisvertmathieu/RTC-GT/FS 

https://www.raspberryme.com/micropython-programmer-esp32-esp8266-a-laide-de-lediteur-mu/ (faire du python sur une ESP32)


https://www.raspberrypi.com/software/ (raspbian)

https://www.youtube.com/watch?v=Vcetxwc5yf8 (utilisation de la raspberry pi sans écran)

https://www.youtube.com/watch?v=aIxZzDWhvvQ&t=155s (ssh)

https://raspberry-pi.fr/connecter-raspberr-pi-port-serie/ (sans internet)

https://www.raspberryme.com/activer-linterface-i2c-sur-le-raspberry-pi/ ( activation I2C raspberry pi 3)

https://br.atsit.in/fr/?p=42438 (utilisation I2C) ( 

https://www.instructables.com/Raspberry-Pi-I2C-Python/ (installation complète I2C raspberry pi 3)

https://osoyoo.com/2016/06/01/drive-i2c-lcd-screen-with-raspberry-pi/ (installation des pins pour l’écran LCD avec la raspberry pi 3)

https://pypi.org/project/RPLCD/ (TUTORIAL FONCTIONNEL pour utilisation de la library I2C python)

https://forums.raspberrypi.com/viewtopic.php?t=115080 (I2C)

https://rplcd.readthedocs.io/en/stable/ (documentation RPCLCD)

https://docs.microsoft.com/fr-fr/windows/iot-core/learn-about-hardware/pinmappings/pinmappingsrpi (mappage des broche GPIO rasberry 3)

https://www.youtube.com/watch?v=cVdSc8VYVBM (nouveau tutoriel (encore une fois..) pour utiliser l’écran LCD avec la raspberry pi..)

https://www.freva.com/fr/comment-connecter-un-ecran-lcd-a-un-raspberry-pi/ ( tuto LCD I2C)

https://www.raspberrypi-spy.co.uk/2018/02/change-raspberry-pi-i2c-bus-speed/ ( 

https://www.youtube.com/watch?v=15XY4LoQyjc (comprendre le bus I2C)

https://www.youtube.com/watch?v=DHbLBTRpTWM&t=351s&ab_channel=MHeidenreich (vidéo pour connecter écran lcd - raspberri)

https://www.dfrobot.com/product-135.html (doc ecran lcd)

https://pinout.xyz/pinout/pin28_gpio1# (mappage précis pin gpio raspi)

https://www.aranacorp.com/fr/programmez-un-esp32-avec-micropython/ (installation micropython)
https://www.youtube.com/watch?v=B8Kr_3xHjqE&list=WL&index=1&t=313s&ab_channel=Tinkernut (vidéo pour connecter i2c)

https://circuitdigest.com/microcontroller-projects/interfacing-i2c-lcd-and-4x4-keypad-with-raspberry-pi-zero-w (tuto comment conneter i2c)

https://raspberry-pi.fr/executer-programme-demarrage/ ( création d’un script pour le lancement du programme au démarrage)

https://www.lojiciels.com/comment-enregistrer-une-tache-cron-dans-ubuntu-2/ (script shell)

https://www.raspberrypi-france.fr/lancer-un-script-python-au-demarrage-du-raspberry-pi/ (script shell)



