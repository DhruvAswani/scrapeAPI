from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Flask routes
@app.route('/')
def index():
    return "Hello, World!"


@app.route('/get_schemes', methods=['GET'])
def get_schemes():
    import requests
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin

    # URL of the page
    url = 'https://wcdhry.gov.in/schemes-for-women/'
    schemes_data = []
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Locate the table body
        table_body = soup.find('tbody')
        if table_body:
            # Find all rows in the table body
            rows = table_body.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) > 3:  # Ensure the row has the expected structure
                    scheme_name = cells[1].get_text(strip=True)  # Extract scheme name
                    link_tag = cells[3].find('a')  # Extract link from the last cell
                    if link_tag and link_tag.has_attr('href'):
                        scheme_link = urljoin(url, link_tag['href'])  # Resolve the relative link
                        schemes_data.append({'name': scheme_name, 'link': scheme_link})

                        print(f"Scheme Name: {scheme_name}")
                        print(f"Scheme Link: {scheme_link}\n")
        else:
            print("Table body not found.")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

    return jsonify({"schemes": schemes_data})


if __name__ == '__main__':
    app.run(debug=True)
