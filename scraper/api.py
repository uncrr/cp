from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import asyncio
import json
import httpx
from scrapers.amazon_scraper import AmazonScraper
from scrapers.creative_scraper import CreativeScraper
from pydantic import BaseModel


class SearchParams(BaseModel):
    search_input: str
    category: str = "all"
    max_price: float
    sort_by: str = "relevant"  # options: relevant, price_low_to_high, price_high_to_low, highest_rating, most_popular

# SORT_MAPPING = {
#     "relevance": "relevant",
#     "price-low": "price_low_to_high", 
#     "price-high": "price_high_to_low",
#     "rating": "highest_rating",
#     "popular": "most_popular"
# }

output_filename = "products.json"

app = FastAPI(title="Creative Scraper API")


async def test_single_scraper(request_body: SearchParams):
    """Test just the amazon scraper to make sure httpx works"""
    scraper = AmazonScraper()
    
    # Simple test search
    search_params = {
        'search_input': request_body.search_input,
        'category': request_body.category,
        'max_price': request_body.max_price,
        'sort_by': request_body.sort_by
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
        print("====================================================================")

    products_data = results
    with open(output_filename, "w") as json_file:
        json.dump(products_data, json_file, indent=4)
    
    return results

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


# Enhanced CORS for Astro development
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:3000", 
#         "http://127.0.0.1:3000",
#         "http://localhost:4321",  # Astro default port
#         "http://127.0.0.1:4321",
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# fetch data from the frontend and return scraped results
@app.post("/api/search")
async def search_products(request_body: SearchParams):
    return await test_single_scraper(request_body)

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "Scraper API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
