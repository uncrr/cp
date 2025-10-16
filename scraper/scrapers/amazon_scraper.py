from . import BaseScraper
import urllib.parse
import httpx

class AmazonScraper(BaseScraper):
    async def scrape(self, params):
        print("🚀 Starting Amazon scrape with httpx...")
        search_url = self.build_url(params)
        
        try:
            html = await self.fetch_page(search_url)
            if html:
                products = self.creative_parse(html, self.get_selectors())
                return {
                    'source': 'amazon',
                    'products': products,
                    'search_params': params
                }
        except Exception as e:
            print(f"💥 Amazon scraping error: {e}")
        
        return {'source': 'amazon', 'products': []}
    
    def build_url(self, params):
        base_url = "https://www.amazon.com/s"
        query = urllib.parse.quote(params['search_input'])
        category_map = {
            'electronics': 'electronics',
            'books': 'stripbooks',
            'home': 'garden',
            'clothing': 'fashion'
        }
        
        category = category_map.get(params['category'], 'aps')
        url = f"{base_url}?k={query}&i={category}"
        
        # Creative sort parameter mapping
        sort_map = {
            'price_low_to_high': 'price-asc-rank',
            'price_high_to_low': 'price-desc-rank',
            'highest_rating': 'review-rank',
            'most_popular': 'popularity-rank',
            'relevant': 'relevance-rank'
        }
        
        if params.get('sort_by') in sort_map:
            url += f"&s={sort_map[params['sort_by']]}"
        
        return url
    
    def get_selectors(self):
        return {
            'product_selectors': [
                'div[data-component-type="s-search-result"]',
                '.s-result-item',
                '.s-main-slot .s-card-container'
            ],
            'title_selectors': [
                'h2 a span',
                '.a-size-medium',
                '.a-text-normal'
            ],
            'price_selectors': [
                '.a-price-whole',
                '.a-offscreen',
                '.a-price .a-offscreen'
            ],
            'rating_selectors': [
                '.a-icon-alt',
                '.a-star-small',
                '.a-size-small .a-color-base'
            ]
        }