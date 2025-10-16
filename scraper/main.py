import asyncio
import httpx
import json
from datetime import datetime
from scrapers.amazon_scraper import AmazonScraper
from scrapers.aliexpress_scraper import AliExpressScraper
from scrapers.alibaba_scraper import AlibabaScraper
from scrapers.walmart_scraper import WalmartScraper
from data_processor import DataProcessor

class CreativeScraper:
    def __init__(self):
        self.scrapers = {
            'amazon': AmazonScraper(),
            'aliexpress': AliExpressScraper(),
            'alibaba': AlibabaScraper(),
            'walmart': WalmartScraper()
        }
        self.processor = DataProcessor()
        
    async def scrape_all(self, search_params):
        """Creative approach: Run all scrapers concurrently with httpx"""
        tasks = []
        
        for site_name, scraper in self.scrapers.items():
            task = self._scrape_with_fallback(scraper, search_params, site_name)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process and merge results
        return self._creative_merge(results, search_params)
    
    async def _scrape_with_fallback(self, scraper, params, site_name):
        """Creative fallback strategy"""
        try:
            return await scraper.scrape(params)
        except Exception as e:
            print(f"Creative fallback for {site_name}: {e}")
            # Try alternative method
            return await self._alternative_scrape_method(scraper, params)
    
    async def _alternative_scrape_method(self, scraper, params):
        """Alternative scraping approach when primary fails"""
        return {"error": "Alternative method not implemented", "source": "fallback"}
    
    def _creative_merge(self, results, search_params):
        """Creatively merge results from different sources"""
        merged_results = []
        
        for result in results:
            if isinstance(result, dict) and 'products' in result:
                processed = self.processor.standardize_data(result['products'], result.get('source'))
                merged_results.extend(processed)
        
        # Apply user filters creatively
        return self._apply_filters_creatively(merged_results, search_params)
    
    def _apply_filters_creatively(self, products, search_params):
        """Apply filters with some creative tolerance"""
        filtered_products = []
        
        for product in products:
            # Creative price matching
            if 'price' in product and search_params.get('max_price'):
                if self._creative_price_match(product['price'], search_params['max_price']):
                    filtered_products.append(product)
            else:
                filtered_products.append(product)
        
        # Creative sorting
        return self._creative_sort(filtered_products, search_params.get('sort_by', 'relevant'))
    
    def _creative_price_match(self, product_price, max_price):
        """Match prices creatively considering different formats and currencies"""
        try:
            # Extract numeric price from string
            price_str = str(product_price).replace('$', '').replace(',', '').split()[0]
            price = float(price_str)
            return price <= max_price * 1.1  # 10% tolerance
        except:
            return True  # Creative: include if price parsing fails
    
    def _creative_sort(self, products, sort_by):
        """Creative sorting based on available data"""
        sort_strategies = {
            'price_low_to_high': lambda x: float(str(x.get('price', 0)).replace('$', '').replace(',', '') or 0),
            'price_high_to_low': lambda x: -float(str(x.get('price', 0)).replace('$', '').replace(',', '') or 0),
            'highest_rating': lambda x: -float(x.get('rating', 0)),
            'most_popular': lambda x: -int(x.get('reviews', 0)),
            'relevant': lambda x: (-float(x.get('rating', 0)), -int(x.get('reviews', 0)))
        }
        
        return sorted(products, key=sort_strategies.get(sort_by, sort_strategies['relevant']))

async def main():
    scraper = CreativeScraper()
    
    # User input simulation
    search_params = {
        'category': 'electronics',
        'search_input': 'wireless headphones',
        'max_price': 100.0,
        'sort_by': 'price_low_to_high'
    }
    
    results = await scraper.scrape_all(search_params)
    
    # Creative output
    print(f"🎯 Found {len(results)} creative results!")
    for product in results[:5]:  # Show first 5
        print(f"📦 {product.get('title', 'N/A')}")
        print(f"   💰 {product.get('price', 'N/A')} | ⭐ {product.get('rating', 'N/A')}")
        print(f"   🏪 {product.get('source', 'N/A')}")
        print("---")

if __name__ == "__main__":
    asyncio.run(main())