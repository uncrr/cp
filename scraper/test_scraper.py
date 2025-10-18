import asyncio
import httpx
from scrapers.amazon_scraper import AmazonScraper

async def test_single_scraper():
    """Test just one scraper to make sure httpx works"""
    scraper = AmazonScraper()
    
    # Simple test search
    search_params = {
        'search_input': 'python programming book',
        'category': 'books',
        'max_price': 1000,
        'sort_by': 'relevant'
    }
    
    print("🧪 Testing Amazon scraper with httpx...")
    
    # Test the fetch_page method directly
    test_url = "https://httpbin.org/user-agent"
    html = await scraper.fetch_page(test_url)
    if html:
        print("✅ httpx is working! Retrieved test page.")
        print("Content preview:", html[:100])
    else:
        print("❌ httpx test failed")
    
    # Test actual scraping
    results = await scraper.scrape(search_params)
    
    print(f"\n📊 Results from {results['source']}:")
    print(f"📦 Found {len(results['products'])} products")
    
    for i, product in enumerate(results['products'][:10], 1):
        print(f"{i}. {product.get('title', 'No title')}")
        print(f"   💰 {product.get('price', 'No price')}")
        print(f"   🔗 {product.get('link', 'No link')}")
        print()

async def test_httpbin():
    """Simple test to verify httpx works"""
    async with httpx.AsyncClient() as client:
        response = await client.get("https://httpbin.org/json")
        if response.status_code == 200:
            print("🎉 httpx is working correctly!")
            data = response.json()
            print(f"Test response: {data['slideshow']['title']}")
        else:
            print(f"❌ httpx test failed: {response.status_code}")

if __name__ == "__main__":
    print("Testing httpx implementation...")
    asyncio.run(test_httpbin())
    print("\n" + "="*50 + "\n")
    asyncio.run(test_single_scraper())