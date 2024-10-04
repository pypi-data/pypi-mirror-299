# test/test_comparateur.py

from pytrackerfr.url_generator.comparateur import ComparateurPreciosURLGenerator

def test_generate_urls_comparateur():
    generator = ComparateurPreciosURLGenerator("test_file.csv")
    params = {
        'domaine_tracking': 'aaa1.client.com',
        'site': 'client-com',
        'nom_support': 'comparateur',
        'nom_campagne': 'été_2024',
        'nom_bannière': 'crea1',
        'url_destination': 'https://www.client.com?param=example'
    }
    urls = generator.générer_urls(params)
    assert len(urls) == 2
    assert 'https://www.client.com?param=example' in urls[0]  # URL de paramètres
