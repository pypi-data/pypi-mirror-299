# url_generator/display.py

from pytrackerfr.url_generator.core import URLGeneratorBase

class DisplayURLGenerator(URLGeneratorBase):
    def valider_paramètres(self, params):
        """Valide les paramètres pour le levier Display."""
        paramètres_obligatoires = ['domaine_tracking', 'site', 'nom_support', 'nom_campagne', 
                                   'nom_emplacement', 'nom_bannière', 'format_bannière', 'url_destination']
        params = {k.strip(): (v.strip() if v is not None else '') for k, v in params.items()}
        
        paramètres_manquants = [param for param in paramètres_obligatoires if param not in params or not params[param]]
        
        if paramètres_manquants:
            raise ValueError(f"Paramètres obligatoires manquants: {', '.join(paramètres_manquants)}")

    def ajuster_pour_cas_spéciaux(self, params):
        """Ajuste les URLs pour des supports spéciaux comme Google, Amazon et Outbrain."""
        nom_support = params['nom_support'].lower()
        
        if 'google' in nom_support:
            params['nom_support'] = 'google-ads'
            params['préfixe_domaine'] = 'https://ew3.io/c/a/'
            params['préfixe_domaine_impression'] = 'https://ew3.io/v/a/'
        elif 'amazon' in nom_support:
            params['nom_support'] = 'Amazon'
            params['préfixe_domaine'] = 'https://ew3.io/c/a/'
            params['préfixe_domaine_impression'] = 'https://ew3.io/v/a/'
        elif 'outbrain' in nom_support:
            params['nom_support'] = 'Outbrain'
            params['préfixe_domaine'] = 'https://ew3.io/c/a/'
            params['préfixe_domaine_impression'] = 'https://ew3.io/v/a/'
        else:
            # Utiliser le domaine de tracking normal si ce n'est pas un cas spécial
            params['préfixe_domaine'] = f"https://{params['domaine_tracking']}/dynclick/"
            params['préfixe_domaine_impression'] = f"https://{params['domaine_tracking']}/dynview/"
        
        return params

    def générer_urls(self, params):
        """Génère les URLs pour le levier Display."""
        params = {k.strip(): (v.strip() if v is not None else '') for k, v in params.items()}
        
        # Ajuster pour Google, Amazon ou Outbrain si nécessaire
        params = self.ajuster_pour_cas_spéciaux(params)

        # URL de paramètres (tracking par URL)
        url_paramètres = (
            f"{params['url_destination']}?ead-publisher={params['nom_support']}&"
            f"ead-name={params['nom_support']}-{params['nom_campagne']}&ead-location={params['nom_emplacement']}-{params['format_bannière']}&"
            f"ead-creative={params['nom_bannière']}-{params['format_bannière']}&ead-creativetype={params['format_bannière']}&"
            f"eseg-name={params.get('nom_segment', '')}&eseg-item={params.get('valeur_segment', '')}&"
            f"ead-mediaplan={params.get('nom_plan_medias', '')}&ea-android-adid={params.get('adid', '')}&ea-ios-idfa={params.get('idfa', '')}"
        )
        
        # URL du pixel d'impression
        url_impression = (
            f'<img src="{params["préfixe_domaine_impression"]}{params["site"]}/1x1.b?'
            f"ead-publisher={params['nom_support']}&ead-name={params['nom_support']}-{params['nom_campagne']}&"
            f"ead-location={params['nom_emplacement']}-{params['format_bannière']}&ead-creative={params['nom_bannière']}-{params['format_bannière']}&"
            f"ead-creativetype={params['format_bannière']}&eseg-name={params.get('nom_segment', '')}&eseg-item={params.get('valeur_segment', '')}&"
            f"ead-mediaplan={params.get('nom_plan_medias', '')}&ea-android-adid={params.get('adid', '')}&ea-ios-idfa={params.get('idfa', '')}&"
            f'ea-rnd=[RANDOM]" border="0" width="1" height="1" />'
        )
        
        return url_paramètres, url_impression
