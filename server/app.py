from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)


def get_soundcloud_data(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        soup = BeautifulSoup(result.content, "html.parser")
        img = soup.find('div').find('img')
        src = (img.get_attribute_list('src')[0]).replace(
            't500x500', 'original')
        title = img.get_attribute_list('alt')[0]
        return {'src': src, 'title': title}
    except requests.exceptions.HTTPError as e:
        raise ValueError('Not a valid Soundcloud link.')
    except requests.exceptions.RequestException as e:
        raise ValueError('Request failed.')
    except (AttributeError, IndexError, KeyError) as e:
        raise ValueError('Error while parsing.')


@app.route('/process_data', methods=['POST'])
def process_data():
    try:
        data = request.json
        url = data.get('link')
        result = get_soundcloud_data(url)
        return jsonify(result)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred.'}), 500


if __name__ == '__main__':
    app.run()
