from abc import ABC, abstractmethod

class BaseScraper(ABC):
    @abstractmethod
    def scrape(self):
        """Returns a list of dicts with title, url, source, scraped_at"""
        pass