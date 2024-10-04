import os
from pytrackeres.url_generator.display import DisplayURLGenerator
from pytrackeres.url_generator.affiliation import AffiliationURLGenerator
from pytrackeres.url_generator.emailing import EmailingURLGenerator
from pytrackeres.url_generator.colaboration import ColaborationURLGenerator
from pytrackeres.url_generator.comparateur import ComparateurPreciosURLGenerator
from pytrackeres.url_generator.google_ads import GoogleAdsURLGenerator
from pytrackeres.url_generator.bing_ads import BingAdsURLGenerator
from pytrackeres.url_generator.social import SocialURLGenerator

# Dictionnaire des templates CSV pour chaque levier
TEMPLATES_CSV = {
    'dy': {
        'headers': "domaine_tracking,site,nom_support,nom_campagne,nom_emplacement,nom_bannière,format_bannière,nom_segment,valeur_segment,url_destination,adid,idfa",
        'mandatory': "oui,oui,oui,oui,oui,oui,oui,non,non,oui,non,non",
        'example': "aaa1.client.com,client-com,amazon,été_2024,ROS,créa1,300x250,,,https://www.client.com?param=example,,"
    },
    'af': {
        'headers': "domaine_tracking,site,nom_support,nom_campagne,nom_bannière,format_bannière,nom_segment,valeur_segment,url_destination,nom_plan_medias,adid,idfa",
        'mandatory': "oui,oui,oui,oui,oui,oui,non,non,oui,non,non,non",
        'example': "aaa1.client.com,client-com,awin,été_2024,créa1,300x250,,,https://www.client.com?param=example,,,"
    },
    'em': {
        'headers': "domaine_tracking,site,nom_support,nom_campagne,mail_utilisateur,nom_segment,valeur_segment,url_destination,nom_plan_medias,id_client,adid,idfa",
        'mandatory': "oui,oui,oui,oui,non,non,non,oui,non,non,non,non",
        'example': "aaa1.client.com,client-com,mailchimp,été_2024,,,,https://www.client.com?param=example,,,,,"
    },
    'co': {
        'headers': "domaine_tracking,site,nom_support,nom_campagne,nom_emplacement,nom_bannière,format_bannière,nom_segment,valeur_segment,url_destination,adid,idfa",
        'mandatory': "oui,oui,oui,oui,oui,oui,oui,non,non,oui,non,non",
        'example': "aaa1.client.com,client-com,partenaire,été_2024,ROS,créa1,300x250,,,https://www.client.com?param=example,,"
    },
    'cp': {
        'headers': "domaine_tracking,site,nom_support,nom_campagne,nom_bannière,nom_segment,valeur_segment,url_destination,nom_plan_medias,adid,idfa",
        'mandatory': "oui,oui,oui,oui,non,non,non,oui,non,non,non,non",
        'example': "aaa1.client.com,client-com,comparateur,été_2024,,,,https://www.client.com?param=example,,,,,"
    },
    'ga': {
        'headers': "domaine_tracking,site,nom_support,nom_campagne,nom_emplacement,nom_bannière,format_bannière,nom_segment,valeur_segment,url_destination,adid,idfa",
        'mandatory': "oui,oui,oui,oui,oui,oui,oui,non,non,oui,non,non",
        'example': "aaa1.client.com,client-com,google-ads,été_2024,ROS,créa1,300x250,,,https://www.client.com?param=example,,"
    },
    'ba': {
        'headers': "domaine_tracking,site,nom_support,nom_campagne,nom_emplacement,nom_bannière,format_bannière,nom_segment,valeur_segment,url_destination,adid,idfa",
        'mandatory': "oui,oui,oui,oui,oui,oui,oui,non,non,oui,non,non",
        'example': "aaa1.client.com,client-com,bing-ads,été_2024,ROS,créa1,300x250,,,https://www.client.com?param=example,,"
    },
    'sc': {
        'headers': "domaine_tracking,site,nom_support,nom_campagne,nom_emplacement,nom_bannière,format_bannière,nom_segment,valeur_segment,url_destination,nom_plan_medias,adid,idfa",
        'mandatory': "oui,oui,oui,oui,oui,oui,oui,non,non,oui,non,non",
        'example': "aaa1.client.com,client-com,facebook,été_2024,ROS,créa1,300x250,,,https://www.client.com?param=example,,,"
    },
}

def afficher_template_csv(levier):
    """Affiche le template CSV pour le levier sélectionné."""
    template = TEMPLATES_CSV.get(levier)
    if template:
        print("\nVoici le template des en-têtes CSV attendu avec un exemple et les champs obligatoires pour ce levier.")
        print(f"\nEN-TÊTES: {template['headers']}")
        print(f"OBLIGATOIRES: {template['mandatory']}")
        print(f"EXEMPLE: {template['example']}\n")
    else:
        print("Aucun template n'est disponible pour ce levier.")

def main(levier_input=None, fichier_input=None):
    if levier_input is None:
        levier_input = input("Indiquez le nom du levier à traiter (dy pour Display, af pour Affiliation, em pour Emailing, co pour Collaboration, cp pour Comparateur de Prix, ga pour Google Ads, ba pour Bing Ads, sc pour Social): ")

    map_levier = {
        'dy': DisplayURLGenerator,
        'af': AffiliationURLGenerator,
        'em': EmailingURLGenerator,
        'co': ColaborationURLGenerator,
        'cp': ComparateurPreciosURLGenerator,
        'ga': GoogleAdsURLGenerator,
        'ba': BingAdsURLGenerator,
        'sc': SocialURLGenerator,
    }

    if levier_input not in map_levier:
        print("Levier introuvable. Veuillez utiliser le code correct.")
        return

    afficher_template_csv(levier_input)

    if fichier_input is None:
        fichier_input = input(r"Veuillez indiquer le chemin complet du fichier CSV. Par exemple C:\\user\\desktop\\données.csv: ")

    if not os.path.exists(fichier_input):
        print(f"Le fichier {fichier_input} n'existe pas.")
        return

    classe_generateur = map_levier[levier_input]
    generateur = classe_generateur(fichier_input)
    generateur.process_csv()

if __name__ == "__main__":
    main()
