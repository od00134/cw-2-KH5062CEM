import requests

# the requests module permits http requests in python 
# by providing ways for making PST, DELETE, GET, PUT and many different http requests

def res(access): # to get resources from the server using the access token

    URL = 'http://localhost:5000/resource'
    headers = {'Authorization': 'Bearer ' + access}
    resp = requests.get(URL, headers = headers)

    if resp.status_code == 200: # if request is True, it returns the json
        return resp.json()
    
    return None # if false, return None

def tokenReq(ID, secret, URL, auth): # function to request an access token from the server

    end = 'http://localhost:8000/token'
    parameters = {'code': auth, 'ID': ID, 'secret': secret, 'URL': URL}
    resp = requests.post(end, data = parameters)

    if resp.status_code == 200: # if request is True, it returns a tuple of token access, type, and expiry
        tknData = resp.json()
        type = tknData.get('type')
        exp = tknData.get('exp')
        access = tknData.get('access')
        return access, type, exp
    
    return None, None, None # if false returns a tuple of three Nones

def req(): # function that requests a token --main function--

    ID = 'ID'
    secret = 'Secret'
    URL = 'http://localhost:8000/callback'
    endpoint = 'http://localhost:8000/authorize'

    # Redirect the user
    autURL = 'http://localhost:8000/authorize?resp_type=code&ID=your_ID&URL=http://localhost:8000/callback'
    print("Please visit the following URL and provide consent:")
    print(autURL)
    
    auth = input("Enter the authorization code: ")

    access, type, exp = tokenReq(ID, secret, URL, auth)

    if access is not None:
        print("Access token:", access)

        resources = res(access)

        if resources is not None:
            print("Resources:")
            print(resources)
        else:
            print("Error in resources access")
    else:
        print("Error in requesting")

# main
req()



