from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

app = Flask(__name__)

# Flask routes
@app.route('/')
def index():
    return "Hello, World!"


@app.route('/get_schemes', methods=['GET'])
def get_schemes():
    url = 'https://wcd.gov.in/'
    response = requests.get(url)
    schemes_data = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        schemes = soup.find_all('a')
        for scheme in schemes:
            if scheme.has_attr('href'):
                scheme_name = scheme.get_text().strip()
                relative_link = scheme['href']
                scheme_link = urljoin(url, relative_link)
                schemes_data.append({'name': scheme_name, 'link': scheme_link})
    else:
        return jsonify({"error": "Failed to retrieve the page", "status": response.status_code}), 500

    return jsonify({"schemes": schemes_data})

if __name__ == '__main__':
    app.run(debug=True)
