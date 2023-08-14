from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/res', methods=['GET'])
def res():
    TKNAccess = request.headers.get('Authorization').split(' ')[1]

    # Validate the access token
    if validate_access_token(TKNAccess):
        return jsonify({'res': ['Omar', 'Ahmad']}), 200
    else:
        return jsonify({'error': 'Invalid token'}), 401


def validate_access_token(TKNAccess):
    oauth_server_url = 'http://localhost:8000/validate_token'  
    response = requests.post(oauth_server_url, json={'TKNAccess': TKNAccess})

    if response.status_code == 200:
        return True
    else:
        return False


if __name__ == '__main__':
    app.run(port=5000)



