
# Générateur d'URLs de Tracking

## Description

Ce projet permet de générer des URLs de tracking pour différents leviers publicitaires, tels que l'Affiliation, Display, Emailing, Comparateur de Prix, Google Ads, Bing Ads, et Social. Chaque levier possède ses propres paramètres obligatoires et des formats spécifiques.

Le projet lit un fichier CSV contenant les paramètres pour chaque levier, valide les paramètres, et génère deux types d'URLs :
1. **URL de Paramètres** : URL utilisée pour le suivi des clics (tracking par paramètres).
2. **URL de Pixel d'Impression** : URL utilisée pour le suivi des impressions.

## Structure du Projet

- `main.py` : Le fichier principal pour lancer la génération d'URLs.
- `core.py` : Contient la logique de base pour lire les fichiers CSV et générer les URLs. C'est ici que se trouve la classe `URLGeneratorBase`, utilisée comme base pour chaque levier.
- Dossiers de leviers :
  - `affiliation.py` : Génère des URLs pour les campagnes d'affiliation.
  - `display.py` : Génère des URLs pour les campagnes display.
  - `emailing.py` : Génère des URLs pour les campagnes emailing.
  - `colaboration.py` : Génère des URLs pour les campagnes de collaboration.
  - `comparateur.py` : Génère des URLs pour les campagnes de comparateurs de prix.
  - `google_ads.py` : Génère des URLs pour les campagnes Google Ads.
  - `bing_ads.py` : Génère des URLs pour les campagnes Bing Ads.
  - `social.py` : Génère des URLs pour les campagnes sociales.

## Utilisation

1. Exécutez le fichier `main.py` :
   ```bash
   python main.py
   ```

2. Sélectionnez le levier à traiter :
   - `dy` pour Display
   - `af` pour Affiliation
   - `em` pour Emailing
   - `co` pour Colaboration
   - `cp` pour Comparateur de Prix
   - `ga` pour Google Ads
   - `ba` pour Bing Ads
   - `sc` pour Social

3. Entrez le chemin complet du fichier CSV.

4. Le programme générera un fichier CSV avec les **URLs de paramètres** et les **URLs de pixel d'impression** pour chaque levier.

## Exemple de Fichier CSV

Voici un exemple de fichier CSV attendu pour le levier d'affiliation :

```csv
domaine_tracking,site,nom_support,nom_campagne,nom_bannière,format_bannière,url_destination
aaa1.client.com,client-com,awin,été_2024,crea1,300x250,https://www.client.com?param=example
```

## Tests

Les tests unitaires sont disponibles dans le dossier `test`. Chaque levier dispose de son propre fichier de tests. Voici les fichiers de tests associés aux différents leviers :

- `test_affiliation.py`
- `test_bing_ads.py`
- `test_colaboration.py`
- `test_comparateur.py`
- `test_display.py`
- `test_emailing.py`
- `test_google_ads.py`
- `test_social.py`

Pour exécuter les tests unitaires :

```bash
pytest
```

Les tests vérifieront que les URLs de paramètres et les URLs d'impression sont générées correctement pour chaque levier.

## Contributions

Les contributions sont les bienvenues. N'hésitez pas à soumettre des PRs pour améliorer le projet ou ajouter de nouveaux leviers de génération d'URLs.

## Licence

Ce projet est sous licence MIT.
