import httpx
from bs4 import BeautifulSoup
import random
import asyncio

class BaseScraper:
    def __init__(self):
        self.headers_list = [
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            },
            {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
        ]
    
    def get_headers(self):
        return random.choice(self.headers_list)
    
    async def fetch_page(self, url, client=None):
        """Creative fetching with retries using httpx"""
        close_client = False
        if client is None:
            client = httpx.AsyncClient(timeout=30.0)
            close_client = True
        
        for attempt in range(3):
            try:
                response = await client.get(url, headers=self.get_headers())
                if response.status_code == 200:
                    if close_client:
                        await client.aclose()
                    return response.text
                elif response.status_code == 429:  # Too many requests
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                await asyncio.sleep(1)
        
        if close_client:
            await client.aclose()
        return None
    
    def creative_parse(self, html, selectors):
        """Creative parsing with BeautifulSoup"""
        soup = BeautifulSoup(html, 'html.parser')
        products = []
        
        # Try different selectors creatively
        for selector in selectors['product_selectors']:
            product_elements = soup.select(selector)
            if product_elements:
                print(f"🎉 Found {len(product_elements)} products with selector: {selector}")
                for element in product_elements[:10]:  # Limit to first 10 for performance
                    product_data = self._extract_product_data(element, selectors)
                    if product_data:
                        products.append(product_data)
                break
        
        return products
    
    def _extract_product_data(self, element, selectors):
        """Extract data creatively with multiple fallbacks"""
        product = {}
        
        # Creative title extraction
        for selector in selectors['title_selectors']:
            title_elem = element.select_one(selector)
            if title_elem:
                product['title'] = title_elem.get_text().strip()
                break
        
        # Creative price extraction
        for selector in selectors['price_selectors']:
            price_elem = element.select_one(selector)
            if price_elem:
                product['price'] = self._clean_price(price_elem.get_text())
                break
        
        # Creative rating extraction
        for selector in selectors['rating_selectors']:
            rating_elem = element.select_one(selector)
            if rating_elem:
                product['rating'] = self._clean_rating(rating_elem.get_text())
                break
        
        # Creative link extraction
        for selector in selectors.get('link_selectors', []):
            link_elem = element.select_one(selector)
            if link_elem and link_elem.has_attr('href'):
                product['link'] = "https://www.amazon.com" + link_elem['href']
                product['source'] = "Amazon"
                break

        for selector in selectors.get('description_selectors', []):
            desc_elem = element.select_one(selector)
            if desc_elem:
                product['description'] = desc_elem.get_text().strip()
                break
        
        for selector in selectors.get('image_selectors', []):
            img_elem = element.select_one(selector)
            if img_elem and img_elem.has_attr('src'):
                product['image'] = "https://www.amazon.com" + img_elem['src']
                break

        for selector in selectors.get('shipping_selectors', []):
            ship_elem = element.select_one(selector)
            if ship_elem:
                product['shipping'] = ship_elem.get_text().strip()
                break
        
        for selector in selectors.get('in_stock_selectors', []):
            stock_elem = element.select_one(selector)
            if stock_elem:
                product['in_stock'] = 'in stock' in stock_elem.get_text().lower()
                break
        
        for selector in selectors.get('vendor_selectors', []):
            vendor_elem = element.select_one(selector)
            if vendor_elem:
                product['vendor'] = vendor_elem.get_text().strip()
                break
        
        for selector in selectors.get('review_count_selectors', []):
            review_elem = element.select_one(selector)
            if review_elem:
                product['review_count'] = self._clean_price(review_elem.get_text())
                break

        for selector in selectors.get('category_selectors', []):
            category_elem = element.select_one(selector)
            if category_elem:
                product['category'] = category_elem.get_text().strip()
                break

        for selector in selectors.get('original_price_selectors', []):
            orig_price_elem = element.select_one(selector)
            if orig_price_elem:
                product['original_price'] = self._clean_price(orig_price_elem.get_text())
                break
        
        return product if product else None
    
    def _clean_price(self, price_text):
        """Creative price cleaning"""
        import re
        # Extract numbers and decimal points
        matches = re.findall(r'[\d,]+\.?\d*', price_text)
        return matches[0] if matches else "0"
    
    def _clean_rating(self, rating_text):
        """Creative rating cleaning"""
        import re
        matches = re.findall(r'[\d\.]+', rating_text)
        return matches[0] if matches else "0"