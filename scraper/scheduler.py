import time
import os
from core.config import ANIME_SHIELD_URL
from database.db_manager import DBManager
from scraper.anime_shield import AnimeShield
from scraper.base_scraper import BaseScraper
from scraper.parser import AnimeParser

class ScraperScheduler:
    def __init__(self, interval_seconds=None):
        self.interval_seconds = interval_seconds or int(
            os.environ.get("SCRAPE_INTERVAL_SECONDS", "600")
        )

    def run_scraping_cycle(self):
        shield = AnimeShield()
        shield.random_delay()
        scraper = BaseScraper(ANIME_SHIELD_URL)
        html = scraper.fetch_page(headers=shield.get_safe_headers())
        if not html:
            print("Scrape failed or target returned no page; existing data was kept.")
            return False

        soup = scraper.parse_content(html)
        items = AnimeParser().parse_anime_list(soup)
        if not items:
            print("No anime items were parsed; existing data was kept.")
            return False

        if DBManager.save_data(items):
            print(f"Saved {len(items)} anime items.")
            return True
        return False

    def run_forever(self):
        while True:
            try:
                print("Starting scraping cycle...")
                self.run_scraping_cycle()
            except Exception as e:
                print(f"Scraping cycle failed: {e}")
            print(f"Next scrape in {self.interval_seconds} seconds.")
            time.sleep(self.interval_seconds)

if __name__ == "__main__":
    ScraperScheduler().run_forever()