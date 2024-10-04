# url_generator/emailing.py

from pytrackerfr.url_generator.core import URLGeneratorBase

class EmailingURLGenerator(URLGeneratorBase):
    def valider_paramètres(self, params):
        """Valide les paramètres pour le levier Emailing."""
        paramètres_obligatoires = ['domaine_tracking', 'site', 'nom_support', 'nom_campagne', 'url_destination']
        params = {k.strip(): (v.strip() if v is not None else '') for k, v in params.items()}
        
        paramètres_manquants = [param for param in paramètres_obligatoires if param not in params or not params[param]]
        
        if paramètres_manquants:
            raise ValueError(f"Paramètres obligatoires manquants: {', '.join(paramètres_manquants)}")

    def générer_urls(self, params):
        """Génère les URLs pour le levier Emailing."""
        params = {k.strip(): (v.strip() if v is not None else '') for k, v in params.items()}

        # URL de paramètres (tracking par URL)
        url_paramètres = (
            f"{params['url_destination']}?eml-publisher={params['nom_support']}&"
            f"eml-name={params['nom_support']}-{params['nom_campagne']}&"
            f"eseg-name={params.get('nom_segment', '')}&eseg-item={params.get('valeur_segment', '')}&"
            f"eml-mediaplan={params.get('nom_plan_medias', '')}&uid={params.get('id_client', '')}&"
            f"ea-android-adid={params.get('adid', '')}&ea-ios-idfa={params.get('idfa', '')}"
        )
        
        # Ajouter mail_utilisateur si présent
        if params.get('mail_utilisateur'):
            url_paramètres += f"&eemail={params['mail_utilisateur']}"
        
        # URL du pixel d'impression
        url_impression = (
            f'<img src="https://{params["domaine_tracking"]}/dynview/{params["site"]}/1x1.b?'
            f"eml-publisher={params['nom_support']}&eml-name={params['nom_support']}-{params['nom_campagne']}&"
            f"eseg-name={params.get('nom_segment', '')}&eseg-item={params.get('valeur_segment', '')}&"
            f"eml-mediaplan={params.get('nom_plan_medias', '')}&uid={params.get('id_client', '')}&"
            f"ea-android-adid={params.get('adid', '')}&ea-ios-idfa={params.get('idfa', '')}&ea-rnd=[RANDOM]\" border=\"0\" width=\"1\" height=\"1\" />"
        )
        
        return url_paramètres, url_impression
