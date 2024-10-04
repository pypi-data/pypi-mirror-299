from abc import ABC, abstractmethod
import urllib.parse
import csv
from datetime import datetime

class URLGeneratorBase(ABC):
    def __init__(self, fichier_input):
        self.fichier_input = fichier_input
        self.urls = []
        self.levier = 'levier_par_défaut'  # Vous pouvez changer cela ou l'attribuer dynamiquement si nécessaire

    @abstractmethod
    def valider_paramètres(self, params):
        """Cette méthode sera implémentée par chaque levier pour valider les paramètres."""
        pass

    @abstractmethod
    def générer_urls(self, params):
        """Cette méthode sera implémentée par chaque levier pour générer les URLs."""
        pass

    def encoder_url(self, url):
        """Encode l'URL de destination."""
        return urllib.parse.quote(url, safe='')

    def traiter_csv(self):
        """Lit le fichier CSV, valide les paramètres et génère les URLs."""
        try:
            with open(self.fichier_input, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row:  # Ignorer toute ligne vide
                        try:
                            # Nettoyer les espaces blancs dans les lignes du CSV et éviter None
                            row = {k.strip(): (v.strip() if v is not None else '') for k, v in row.items() if k and v}
                            
                            # Traiter uniquement s'il y a suffisamment de valeurs dans la ligne
                            if row:
                                self.valider_paramètres(row)  # Valider les paramètres
                                url_impression, url_paramètres = self.générer_urls(row)
                                self.urls.append({
                                    'URL de Paramètres': url_paramètres,
                                    'URL de Pixel d’Impression': url_impression
                                })
                        except ValueError as e:
                            print(f"Erreur dans la ligne: {row} - {str(e)}")
        except FileNotFoundError:
            print(f"Le fichier {self.fichier_input} n'existe pas.")
        except Exception as e:
            print(f"Une erreur s'est produite lors du traitement du fichier: {str(e)}")

        self.écrire_csv()

    def générer_nom_fichier_sortie(self):
        """Génère un nom de fichier de sortie unique avec la date, l'heure et le levier."""
        now = datetime.now()
        timestamp = now.strftime("%Y_%m_%d_%H_%M_%S")
        return f"{timestamp}_urls_{self.levier}_générées.csv"

    def écrire_csv(self):
        """Écrit les URLs générées dans un fichier CSV."""
        fichier_sortie = self.générer_nom_fichier_sortie()  # Utiliser un nom avec un timestamp
        try:
            with open(fichier_sortie, mode='w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['URL de Paramètres', 'URL de Pixel d’Impression']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for url in self.urls:
                    writer.writerow(url)
            
            print(f"Les URLs générées ont été enregistrées dans {fichier_sortie}.")
        except Exception as e:
            print(f"Erreur lors de l'écriture du fichier: {str(e)}")
