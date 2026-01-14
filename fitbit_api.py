import json
import requests
from datetime import datetime, timedelta


class FitbitAPI:
    #class constructor
    def __init__(self):
        self.load_tokens()
        self.check_token_expiry()
        
    #gets data from fitbit
    def make_request(self, endpoint):
        my_url = f"https://api.fitbit.com/1/{endpoint}"
        my_headers = {"Authorization": f"Bearer {self.access_token}"}
        
        response = requests.get(my_url, headers = my_headers)
        
        #error handling logic 
        if response.status_code != 200:
            print(f"API Error {response.status_code}: {response.text}")
            
            #token expiration error (#401)
            if response.status_code == 401:
                self.refresh_token()
                
        
        
        
        return response.json()
    
    #steps
    def get_steps(self, start_date, end_date):
        return self.make_request(f"user/-/activities/steps/date/{start_date}/{end_date}.json")
    
    #heart rate
    def get_heart_rate(self, start_date, end_date):
        return self.make_request(f"user/-/activities/heart/date/{start_date}/{end_date}.json")
    
