import os # access env variables such as FITBIT_CLIENT_ID
from dotenv import load_dotenv # lets us read from .env
import urllib.parse # for building urls
from flask import Flask, request
import requests #making requests to http
import base64 #encoding client_id and secret into base64 for lord fitbit
import threading 
import json

# loads the variables from .env into the actual environment
load_dotenv()

# grab the variables that OAuth wants
CLIENT_ID = os.getenv("FITBIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("FITBIT_CLIENT_SECRET")
REDIRECT_URI = os.getenv("FITBIT_REDIRECT_URI")

##########################################################

def start_auth_flow():
    #opens fitbit login page in the new browser
    #will be able to call this function from ui.py!
    import webbrowser
    print("\nOpening Fitbit Login Page")
    webbrowser.open(auth_url)
    
def start_server():
    """Run Flask in a background thread so PyQt stays responsive."""
    thread = threading.Thread(target=lambda: app.run(port=8080, debug=True, use_reloader=False))
    thread.daemon = True
    thread.start()

#function that gets the token 
def exchange_code_for_token(auth_code):
    #fitbit token URL grabber
    TOKEN_URL = "https://api.fitbit.com/oauth2/token"
    
    #funky base64 format
    client_creds = f"{CLIENT_ID}:{CLIENT_SECRET}"
    client_creds_b64 = base64.b64encode(client_creds.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {client_creds_b64}", #our credentials
        "Content-Type":"application/x-www-form-urlencoded" 
    }
    
    #POST is a protocol used to send data to a server
    
    #POST data: 
    data = {
        "client_id": CLIENT_ID,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
        "code": auth_code
    }
    
    #POST request
    response = requests.post(TOKEN_URL, headers=headers, data=data)
    
    #convert the response we get into JSON
    token_data = response.json()
    
    #stuff for debugging
    print("\n==== TOKEN RESPONSE FROM FITBIT ====")
    print(token_data)
    print("===================================")
    
    return token_data

def save_tokens(token_data):
    #opens a json file named tokens.json
    #cont... w = we are writing to it, saved as variable called f
    with open("tokens.json", "w") as f: 
        json.dump(token_data, f, indent = 4) #puts the data in here
        
def load_tokens():
    with open("tokens.json", "r") as f:
        return json.load(f)

################################################################

#print confirmation that these were loaded to terminal
print("Client ID loaded: ", CLIENT_ID)
print("Redirect URI loaded: ", REDIRECT_URI)

AUTH_URL = "https://www.fitbit.com/oauth2/authorize"

#parameters that fitbit wants
params = {
    "response_type": "code",
    "client_id": CLIENT_ID,
    "redirect_uri": REDIRECT_URI,
    "scope": "activity heartrate sleep profile", #for now...    
}

#build full URL including parameters
auth_url = AUTH_URL + "?" + urllib.parse.urlencode(params)

#print to console for now, will switch to automated with button later.. 
print("\n Open this URL in browser to login with fitbit")
print(auth_url)

#constructor... FLASK LINKS MY CODE AND FUNCTIONS TO THE WEBSITES!!!
app = Flask(__name__)

@app.route("/callback") #makes client go to callback function
def callback():
    code = request.args.get("code")
    print("\n Authorization code get!: ", code)
    
    token_data = exchange_code_for_token(code)
    access_token = token_data.get("access_token")
    
    save_tokens(access_token)
    print("\nYour Access Token: ", access_token)
    return "auth success! close this window and return to app"

if __name__ == "__main__": #runs to redirect uri: http://localhost:8000/callback
    app.run(port = 8080, debug = True)