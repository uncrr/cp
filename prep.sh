#!/bin/sh

# Setup python venv and Install requirements
cd ./scraper/ && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# Install dependencies for Astro UI
cd ./ui && npm install