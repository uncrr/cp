#!/bin/sh

cd ./scraper && 

# Run the python scraper wit reload and fetch results to products.json
# from http://localhost:8000/api/search
uvicorn api:app --reload --host 0.0.0.0 --port 8000 &

# Keep waiting
wait