import time
import threading
from database.db_manager import DBManager
from scraper.anime_shield import AnimeShield

class ScraperScheduler:
    def __init__(self):
        print("Scraper Scheduler initialized!")

    def run_scraping_cycle(self):
        while True:
            try:
                print("Starting background scraping cycle...")
                scraper = AnimeShield()
                scraped_data = scraper.fetch_data() # या जो भी तेरा फेच करने का मेथड हो
                
                if scraped_data:
                    DBManager.save_data(scraped_data)
                    print("Data successfully scraped and saved to database!")
                else:
                    print("No data fetched in this cycle.")
            except Exception as e:
                print(f"Error in scraping cycle: {e}")
            
            # हर 10 मिनट बाद दोबारा डेटा फेच करेगा
            time.sleep(600)

    def start_background_thread(self):
        thread = threading.Thread(target=self.run_scraping_cycle, daemon=True)
        thread.start()
        print("Background scraper thread started successfully!")

print("Scheduler script ready!")