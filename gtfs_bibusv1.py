"""
Description: Programme écrit dans le langage de programmation Python3, permettant à une raspberry pi (3) de recevoir des données du centre de données
Bibus, de les mettre dans le format gtfs-rt puis d'afficher ses données sur un écran LCD avec les arrêts souhaiter. 
Objectif:  Afficher la direction et le temps d'arrivée en minute de l'arrêt Bouguen.
Matériel: 
- Raspberry pi 3
- Ecran LCD DFROBOT x
- Câble USB
- Connexion à internet 
- Fils de connexion (minimum 4)
Auteurs: Harrison Misy, Ange Leyrit, Joselin Scouarnec
Date: 15/04/2022.
Version: 1.0.
"""

######/Configuration/#######
## Importe les modules nécessaire au fonctionnement du programme
from time import sleep
sleep(60)
from datetime import datetime, timedelta
import csv
import urllib.request
import drivers
from google.transit import gtfs_realtime_pb2 as gtfs

#Url permettant de récuperer le fichiers GTFS-RT trip_update
url_data_bibus = "https://www.data.gouv.fr/fr/datasets/r/f7cbc4f8-da19-4bf3-8c88-c4afda0090a4"

#Définition des arrêt dont on veut les temps d'arrivées des bus
arret=["BOUGUE_1","BOUGUE_2","BOUGUE_3"]

#Récupération des informations statiques sur les trajets et arrêts
trip_meta = "trips.csv"
stop_meta = "stops.csv"

#Définition du temps limite d'arrivée des bus pour qu'il soit afficher en minute, exemple : Les arrivées supérieurs à 60 minutes ne seront pas afficher.
limite = 60

def obtenirMAJ(url, arret): #Fonction de récupération et d'organisation des données du GTFS-RT trip_update

    # Definition d'un message de flux qui consiste en une réponse à une requête HTTP GET au serveur Bibus
    feed = gtfs.FeedMessage()

    # Prendre les données de l'url et les met dans reponse.
    reponse = urllib.request.urlopen(url)

    # Met reponse sous forme d'une chaine de caracteres
    feed.ParseFromString(reponse.read())

    # Dictionnaire contenant notre mise à jour des horaires.
    MAJ_horaire=[]

    #Parcours des différentes classes structurant le fichiers trip_update
    for entity in feed.entity:

        for update in entity.trip_update.stop_time_update: 

            if update.stop_id in arret :#Si il y a une correspondance entre l'arret du fichiers et un des arret déclarer en config.

                MAJ_horaire.append({'stop': update.stop_id,
                                'trip': entity.trip_update.trip.trip_id,
                                'time': update.arrival.time
                                })#On ajoute l'arret, le trajet, et le temps d'arrivées estimer dans notre MAJ

    return MAJ_horaire # Retourne le dictionnaire mis à jour

def find(dic, key, match): #Fonction qui permet de trouver dans un dictionnaire une information rechercher
    for row in dic :
        if row[key] == match :
            return row
    
    raise Exception(f"Not found  {dic}[{key}] : {match}") # Si il ne trouve pas de correspondance retourne une erreur


def Affichage_MAJ(update, limite): #Fonction d'affichage de l'horaire sur le terminal de l'IDE Python et un écran lcd

    # Definit un écran LCD avec le module drivers
    display = drivers.Lcd()

    # Definit une variable maintenant qui est le temps présent au format UTC
    maintenant = datetime.now()

    # Definit une variable arrivee qui est le temps d'arrivee au format UTC
    arrivee = datetime.utcfromtimestamp(update['time'])
    
    # Definit une variable difference qui est la difference de arrivee et de maintenant on sait donc combien de temps il reste avant que le bus arrive
    difference = arrivee-maintenant

    # Definit une variable en_minute qui prend le temps en seconde et le convertit en minute entiere
    en_minute = difference.seconds // 60
    
    # Si le temps darrive et inferieur au temps en minute alors le bus est passé, ou si le temps en minute et superieur à la limite qu'on a choisit alors le bus arrive dans un temps trop long
    if arrivee < maintenant or en_minute > limite:
        return # Arret de Affichage_MAJ
    
    # Definit des variables qui ont pour valeur la clé rechercher. 
    trip = find(rtrip, 'trip_id', update['trip'])
    stop = find(rstop, 'stop_id', update['stop'])

    # Si le temps d'arrivee en minute et inférieur ou égale à 1 alors affiche 'Arrive Imminente'
    if en_minute<=1:
        # Affiche sur l'écran LCD à la ligne 1, le numéro de ligne et la direction
        display.lcd_display_string(f"{trip['route_id']} {trip['trip_headsign']}", 1)

        # Affiche sur l'écran LCD à la ligne 2 'Arrive Imminente'
        display.lcd_display_string(f"Arrive Imminente", 2)

        #Laisse l'affichage pendant 4 secondes
        sleep(4)

        # Affiche dans la console l'arrêt, le numéro de ligne, la direction et 'Arrive Imminente'
        print(f"Arrêt {stop['stop_name']}",
          f"Ligne {trip['route_id']} -  Direction :{trip['trip_headsign']}" ,
          f" Arrive Imminente",sep=',')
    
    #Sinon (si le temps d'arrivee > 1), alors affiche le temps d'arrivee en minute
    else :

        # Affiche sur l'écran LCD à la ligne 1, le numéro de ligne et la direction
        display.lcd_display_string(f"{trip['route_id']} {trip['trip_headsign']}", 1)

        # Affiche sur l'écran LCD à la ligne 2 le temps d'arrivee en minute
        display.lcd_display_string(f"Arrive dans {en_minute}min", 2)

        ##Laisse l'affichage pendant 4 secondes
        sleep(4)

        # Affiche dans la console l'arrêt, le numéro de ligne, la direction et 'Arrive Imminente'
        print(f"Arrêt {stop['stop_name']}",
          f"Ligne {trip['route_id']} - Direction: {trip['trip_headsign']} ",
          f" Arrive dans {en_minute}min",sep=',')


# Permet d'avoir un main
if __name__ == "__main__" :
    #Création des dictionnaires qui permetteront de matcher les fichiers GFTS et GFTS-RT
    with open(trip_meta, 'r') as ftrip, open(stop_meta, 'r') as fstop:
        rtrip = list(csv.DictReader(ftrip))
        rstop = list(csv.DictReader(fstop)) 

    display = drivers.Lcd()#Initialisation de l'écran

    # Boucle ∞ 
    while True:

        #Récupération et organisation des données dans un tableaux updates
        updates = obtenirMAJ(url_data_bibus, arret)

        #Supprime toutes les informations sur l'écran LCD    
        display.lcd_clear()
        
        #Boucle d'affichage des temps d'arrivées de bus avec leur ligne et direction, affichage du bus arrivant le plus tot au plus tard 
        for update in sorted(updates, key=lambda u:u['time']):
            Affichage_MAJ(update,limite)

      
   
   

             
        
    

 