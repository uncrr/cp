#!/bin/sh

# Run the python scraper once and fetch results to products.json
cd ./scraper && python3 main.py &

# Start User interface with live reload
cd ./ui && npm run dev &

# Keep running
wait