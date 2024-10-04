# test/test_social.py

from pytrackerfr.url_generator.social import SocialURLGenerator

def test_generate_urls_social():
    generator = SocialURLGenerator("test_file.csv")
    params = {
        'domaine_tracking': 'aaa1.client.com',
        'site': 'client-com',
        'nom_support': 'facebook',
        'nom_campagne': 'été_2024',
        'nom_emplacement': 'ROS',
        'nom_bannière': 'crea1',
        'format_bannière': '300x250',
        'url_destination': 'https://www.client.com?param=example'
    }
    urls = generator.générer_urls(params)
    assert len(urls) == 2
    assert 'https://www.client.com?param=example' in urls[0]  # URL de paramètres
