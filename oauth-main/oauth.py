from flask import Flask, jsonify, request
import secrets
import string

app = Flask(__name__)

authCodes = {}

stored_tknAccesss = {}

@app.route('/authorize', methods=['GET'])
def authorize():
    ID = request.args.get('ID')

    # Verify the client
    if ID == 'ID':
        return '''
        <html>
        <head>
            <title>Consent page</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                }}
                h1 {{
                    color: #333;
                }}
                .container {{
                    max-width: 400px;
                    margin: 0 auto;
                    padding: 20px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    background-color: #f9f9f9;
                }}
                .btn {{
                    display: inline-block;
                    padding: 8px 16px;
                    font-size: 14px;
                    font-weight: bold;
                    text-decoration: none;
                    color: #fff;
                    background-color: #007bff;
                    border-radius: 5px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Consent page</h1>
                <p>Click the "Verify" button to authorize.</p>
                <form action="/callback" method="post">
                    <input type="hidden" name="ID" value="{0}">
                    <input class="btn" type="submit" value="Verify">
                </form>
            </div>
        </body>
        </html>
        '''.format(ID)
    else:
        return jsonify({'error': 'Invalid client'}), 401

@app.route('/callback', methods=['POST'])
def callback():
    ID = request.form.get('ID')

    authCode = genAuthCode()

    authCodes[ID] = authCode

    return '''
    <html>
    <head>
        <title>Authorization Code</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
            }}
            h1 {{
                color: #333;
            }}
            .container {{
                max-width: 400px;
                margin: 0 auto;
                padding: 20px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #f9f9f9;
            }}
            .code-label {{
                font-size: 16px;
                margin-bottom: 10px;
            }}
            .code-value {{
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                background-color: #f1f1f1;
                border-radius: 5px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Authorization Code</h1>
            <p>Your authorization code is:</p>
            <div class="code-value">{0}</div>
        </div>
    </body>
    </html>
    '''.format(authCode)

@app.route('/token', methods=['POST'])
def exchange():
    authCode = request.form.get('code')
    ID = request.form.get('ID')
    secret = request.form.get('secret')

    if ID != 'ID' or secret != 'secret':
        return jsonify({'error': 'Invalid client credentials'}), 401

    stored_auth_code = authCodes.get(ID)
    if stored_auth_code != authCode:
        return jsonify({'error': 'Invalid authorization code'}), 400

    def genAccessTkn(length=32):

        characters = string.ascii_letters + string.digits

        token = ''.join(secrets.choice(characters) for _ in range(length))

        return token

    def genTknResp():
        tknAccess = genAccessTkn()
        type = 'bearer'
        exp = 3600

        stored_tknAccesss[tknAccess] = {
            'ID': ID,
            'exp': exp
        }

        return jsonify({'tknAccess': tknAccess, 'type': type, 'exp': exp})

    response = genTknResp()
    return response

@app.route('/validation', methods=['POST'])
def validation():
    tknAccess = request.json.get('tknAccess')

    if tknAccess in stored_tknAccesss:
        return jsonify({'status': 'valid'}), 200
    
    return jsonify({'status': 'invalid'}), 401


def genAuthCode(length=16):
    characters = string.ascii_letters + string.digits

    code = ''.join(secrets.choice(characters) for _ in range(length))

    return code

if __name__ == '__main__':
    app.run(port=8000)


