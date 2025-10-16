import re
import json

class DataProcessor:
    def __init__(self):
        self.source_processors = {
            'amazon': self._process_amazon,
            'aliexpress': self._process_aliexpress,
            'alibaba': self._process_alibaba,
            'walmart': self._process_walmart
        }
    
    def standardize_data(self, products, source):
        """Convert all products to standardized format"""
        processor = self.source_processors.get(source, self._process_generic)
        return [processor(product) for product in products if product]
    
    def _process_amazon(self, product):
        return {
            'title': product.get('title', 'Unknown Product'),
            'price': f"${product.get('price', '0')}",
            'rating': product.get('rating', '0').split()[0] if 'rating' in product else '0',
            'reviews': '0',
            'source': 'Amazon',
            'url': '#',
            'image': '#'
        }
    
    def _process_alibaba(self, product):
        price = product.get('price', '0')
        if '-' in str(price):
            price = str(price).split('-')[0]
        
        return {
            'title': product.get('title', 'Unknown Product'),
            'price': f"${price}",
            'rating': product.get('rating', '0'),
            'reviews': '0',
            'source': 'Alibaba',
            'url': '#',
            'image': '#',
            'moq': '1'
        }
    
    def _process_generic(self, product):
        return {
            'title': product.get('title', 'Unknown Product'),
            'price': str(product.get('price', '0')),
            'rating': str(product.get('rating', '0')),
            'reviews': '0',
            'source': 'Unknown',
            'url': '#',
            'image': '#'
        }
    
    def _process_aliexpress(self, product):
        return self._process_generic(product)
    
    def _process_walmart(self, product):
        return self._process_generic(product)