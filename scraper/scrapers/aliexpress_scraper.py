from . import BaseScraper
import urllib.parse

class AliExpressScraper(BaseScraper):
    async def scrape(self, params):
        print("⚠️ AliExpress scraper not yet implemented")
        return {'source': 'aliexpress', 'products': []}