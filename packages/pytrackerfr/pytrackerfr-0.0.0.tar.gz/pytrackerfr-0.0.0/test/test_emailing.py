# test/test_emailing.py

from pytrackerfr.url_generator.emailing import EmailingURLGenerator

def test_generate_urls_emailing():
    generator = EmailingURLGenerator("test_file.csv")
    params = {
        'domaine_tracking': 'aaa1.client.com',
        'site': 'client-com',
        'nom_support': 'mailchimp',
        'nom_campagne': 'été_2024',
        'url_destination': 'https://www.client.com?param=example'
    }
    urls = generator.générer_urls(params)
    assert len(urls) == 2
    assert 'https://www.client.com?param=example' in urls[0]  # URL de paramètres
