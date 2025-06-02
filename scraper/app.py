import requests
import os
from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
from datetime import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pyvirtualdisplay import Display
from fake_useragent import UserAgent
import re

load_dotenv()

app = Flask(__name__)
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

@app.route('/news', methods=['GET'])
def get_news():
    query = request.args.get('q')
    domain = request.args.get('domain')  # Optional parameter

    if not query:
        return jsonify({'error': 'Missing required query parameter: q'}), 400

    url = "https://newsapi.org/v2/everything"
    params = {
        'q': query,
        'apiKey': NEWS_API_KEY
    }

    if domain:
        params['domains'] = domain

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch data from NewsAPI', 'details': response.json()}), response.status_code

    return jsonify(response.json())

@app.route('/scrape_content', methods=['POST'])
def scrape_and_save_md():
    data = request.get_json()
    url = data.get('url')
    safe_url = re.sub(r'[^a-zA-Z0-9]', '_', url)  # Replace non-alphanumeric chars
    filename = f"{safe_url[:100]}.md"  # Truncate to avoid overly long filenames

    if not url:
        return jsonify({'error': 'Missing "url" in request body'}), 400

    storage_dir = "file_storage"
    os.makedirs(storage_dir, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = os.path.join(storage_dir, filename)

    try:
        # Start virtual display (important for Docker and headful mode)
        with Display(visible=0, size=(1280, 720)):
            ua = UserAgent()
            user_agent = ua.random  # Randomized User-Agent

            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)
                context = browser.new_context(user_agent=user_agent)
                page = context.new_page()

                page.goto(url, timeout=60000, wait_until="load")
                content = page.content()

                browser.close()

                soup = BeautifulSoup(content, 'html.parser')
                text = soup.get_text(separator="\n")

                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(f"# Scraped Content from {url}\n\n")
                    f.write(text)

    except Exception as e:
        return jsonify({'error': f'Failed to scrape: {str(e)}'}), 500

    print(f"Saved scraped content to {output_path}")
    return jsonify({'message': 'Scraping complete', 'filename': filename, 'path': output_path, 'content': text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006)
