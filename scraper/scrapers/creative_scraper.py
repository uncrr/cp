import asyncio
import httpx
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
        print(f"🎯 Starting scrape with params: {search_params}")
        
        tasks = []
        for site_name, scraper in self.scrapers.items():
            task = self._scrape_with_fallback(scraper, search_params, site_name)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process and merge results
        final_results = self._creative_merge(results, search_params)
        print(f"✅ Scraping complete. Found {len(final_results)} products")
        return final_results
    
    async def _scrape_with_fallback(self, scraper, params, site_name):
        """Creative fallback strategy"""
        try:
            return await scraper.scrape(params)
        except Exception as e:
            print(f"⚠️ Fallback for {site_name}: {e}")
            return {"source": site_name, "products": [], "error": str(e)}
    
    def _creative_merge(self, results, search_params):
        """Creatively merge results from different sources"""
        merged_results = []
        
        for result in results:
            if isinstance(result, dict) and 'products' in result:
                processed = self.processor.standardize_data(result['products'], result.get('source'))
                merged_results.extend(processed)
        
        return self._apply_filters_creatively(merged_results, search_params)
    
    def _apply_filters_creatively(self, products, search_params):
        """Apply filters with creative tolerance"""
        if not products:
            return []
            
        filtered_products = []
        
        for product in products:
            # Creative price matching
            if 'price' in product and search_params.get('max_price'):
                try:
                    price_str = str(product['price']).replace('$', '').replace(',', '').split()[0]
                    price = float(price_str)
                    if price <= search_params['max_price'] * 1.1:  # 10% tolerance
                        filtered_products.append(product)
                except (ValueError, IndexError):
                    # If price parsing fails, include the product creatively
                    filtered_products.append(product)
            else:
                filtered_products.append(product)
        
        # Creative sorting
        return self._creative_sort(filtered_products, search_params.get('sort_by', 'relevant'))
    
    def _creative_sort(self, products, sort_by):
        """Creative sorting based on available data"""
        if not products:
            return []
            
        sort_strategies = {
            'price_low_to_high': lambda x: float(str(x.get('price', 0)).replace('$', '').replace(',', '') or 0),
            'price_high_to_low': lambda x: -float(str(x.get('price', 0)).replace('$', '').replace(',', '') or 0),
            'highest_rating': lambda x: -float(x.get('rating', 0)),
            'most_popular': lambda x: -int(x.get('reviews', 0)),
            'relevant': lambda x: (-float(x.get('rating', 0)), -int(x.get('reviews', 0)))
        }
        
        try:
            return sorted(products, key=sort_strategies.get(sort_by, sort_strategies['relevant']))
        except Exception as e:
            print(f"⚠️ Sorting error: {e}, returning unsorted")
            return products