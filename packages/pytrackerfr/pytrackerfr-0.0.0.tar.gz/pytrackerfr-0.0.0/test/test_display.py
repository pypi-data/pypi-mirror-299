# test/test_display.py

from pytrackerfr.url_generator.display import DisplayURLGenerator

def test_generate_urls_display_amazon():
    generator = DisplayURLGenerator("test_file.csv")
    params = {
        'domaine_tracking': 'aaa1.client.com',
        'site': 'client-com',
        'nom_support': 'Amazon',
        'nom_campagne': 'été_2024',
        'nom_emplacement': 'ROS',
        'nom_bannière': 'crea1',
        'format_bannière': '300x250',
        'url_destination': 'https://www.client.com?param=example'
    }
    urls = generator.générer_urls(params)
    assert len(urls) == 2
    assert 'https://www.client.com?param=example' in urls[0]  # URL de paramètres

def test_generate_urls_display_outbrain():
    generator = DisplayURLGenerator("test_file.csv")
    params = {
        'domaine_tracking': 'aaa1.client.com',
        'site': 'client-com',
        'nom_support': 'Outbrain',
        'nom_campagne': 'été_2024',
        'nom_emplacement': 'ROS',
        'nom_bannière': 'crea1',
        'format_bannière': '300x250',
        'url_destination': 'https://www.client.com?param=example'
    }
    urls = generator.générer_urls(params)
    assert len(urls) == 2
    assert 'https://www.client.com?param=example' in urls[0]  # URL de paramètres

def test_generate_urls_display_google_ads():
    generator = DisplayURLGenerator("test_file.csv")
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

def test_generate_urls_display_default():
    generator = DisplayURLGenerator("test_file.csv")
    params = {
        'domaine_tracking': 'aaa1.client.com',
        'site': 'client-com',
        'nom_support': 'generic',
        'nom_campagne': 'été_2024',
        'nom_emplacement': 'ROS',
        'nom_bannière': 'crea1',
        'format_bannière': '300x250',
        'url_destination': 'https://www.client.com?param=example'
    }
    urls = generator.générer_urls(params)
    assert len(urls) == 2
    assert 'https://www.client.com?param=example' in urls[0]  # URL de paramètres
