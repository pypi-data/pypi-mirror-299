# test/test_bing_ads.py

from pytrackerfr.url_generator.bing_ads import BingAdsURLGenerator

def test_generate_urls_bing_ads():
    generator = BingAdsURLGenerator("test_file.csv")
    params = {
        'domaine_tracking': 'aaa1.client.com',
        'site': 'client-com',
        'nom_support': 'bing-ads',
        'nom_campagne': 'été_2024',
        'nom_emplacement': 'ROS',
        'nom_bannière': 'crea1',
        'format_bannière': '300x250',
        'url_destination': 'https://www.client.com?param=example'
    }
    urls = generator.générer_urls(params)
    assert len(urls) == 2
    assert 'https://www.client.com?param=example' in urls[0]  # URL de paramètres
