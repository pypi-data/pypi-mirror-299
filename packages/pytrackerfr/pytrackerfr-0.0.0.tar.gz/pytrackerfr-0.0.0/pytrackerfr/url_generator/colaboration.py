# url_generator/colaboration.py

from pytrackerfr.url_generator.core import URLGeneratorBase

class ColaborationURLGenerator(URLGeneratorBase):
    def valider_paramètres(self, params):
        """Valide les paramètres pour le levier Colaboration."""
        paramètres_obligatoires = ['domaine_tracking', 'site', 'nom_support', 'nom_campagne',
                                   'nom_emplacement', 'nom_bannière', 'format_bannière', 'url_destination']
        params = {k.strip(): (v.strip() if v is not None else '') for k, v in params.items()}
        
        paramètres_manquants = [param for param in paramètres_obligatoires if param not in params or not params[param]]
        
        if paramètres_manquants:
            raise ValueError(f"Paramètres obligatoires manquants: {', '.join(paramètres_manquants)}")

    def générer_urls(self, params):
        """Génère les URLs pour le levier Colaboration."""
        params = {k.strip(): (v.strip() if v is not None else '') for k, v in params.items()}

        # URL de paramètres (tracking par URL)
        url_paramètres = (
            f"{params['url_destination']}?colab-publisher={params['nom_support']}&"
            f"colab-name={params['nom_support']}-{params['nom_campagne']}&colab-location={params['nom_emplacement']}-{params['format_bannière']}&"
            f"colab-creative={params['nom_bannière']}-{params['format_bannière']}&colab-creativetype={params['format_bannière']}&"
            f"eseg-name={params.get('nom_segment', '')}&eseg-item={params.get('valeur_segment', '')}&"
            f"colab-mediaplan={params.get('nom_plan_medias', '')}&ea-android-adid={params.get('adid', '')}&ea-ios-idfa={params.get('idfa', '')}"
        )
        
        # URL du pixel d'impression
        url_impression = (
            f'<img src="https://{params["domaine_tracking"]}/dynview/{params["site"]}/1x1.b?'
            f"colab-publisher={params['nom_support']}&colab-name={params['nom_support']}-{params['nom_campagne']}&"
            f"colab-location={params['nom_emplacement']}-{params['format_bannière']}&colab-creative={params['nom_bannière']}-{params['format_bannière']}&"
            f"colab-creativetype={params['format_bannière']}&eseg-name={params.get('nom_segment', '')}&eseg-item={params.get('valeur_segment', '')}&"
            f"colab-mediaplan={params.get('nom_plan_medias', '')}&ea-android-adid={params.get('adid', '')}&ea-ios-idfa={params.get('idfa', '')}&"
            f'ea-rnd=[RANDOM]" border="0" width="1" height="1" />'
        )
        
        return url_paramètres, url_impression
