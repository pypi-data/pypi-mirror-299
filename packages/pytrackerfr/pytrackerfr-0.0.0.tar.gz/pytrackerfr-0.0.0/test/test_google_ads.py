# test/test_google_ads.py

from pytrackerfr.url_generator.google_ads import GoogleAdsURLGenerator

def test_generate_urls_google_ads():
    generator = GoogleAdsURLGenerator("test_file.csv")
    params = {
        'domaine_tracking': 'aaa1.client.com',
        'site': 'client-com',
        'nom_support': 'google-ads',
        'nom_campagne': 'été_2024',
        'nom_emplacement': 'ROS',
        'nom_bannière': 'crea1',
        'format_bannière': '300x250',
        'url_destination': 'https://www.client.com?param=example'
    }
    urls = generator.générer_urls(params)
    assert len(urls) == 2
    assert 'https://www.client.com?param=example' in urls[0]  # URL de paramètres
