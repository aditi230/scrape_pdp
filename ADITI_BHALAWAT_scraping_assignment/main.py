from scrape.foreign_fortune_scraper import ForeignFortuneScraper
from scrape.lechocolat_alainducasse_scraper import LeChocolatAlainDucasseScraper
from scrape.trader_joes_scraper import TraderJoesScraper

class ScraperManager:
    def __init__(self):
        self.scraper_instances = [
            ForeignFortuneScraper(),
            LeChocolatAlainDucasseScraper(),
            TraderJoesScraper()
        ]

    def run_scrapers(self):
        for scraper in self.scraper_instances:
            print(f"Running scraper: {scraper.__class__.__name__} This may take few minutes")
            scraper.scrape()
            print(f"Finished scraper: {scraper.__class__.__name__}. Kindly see result in output directry")

if __name__ == "__main__":
    manager = ScraperManager()
    manager.run_scrapers()
