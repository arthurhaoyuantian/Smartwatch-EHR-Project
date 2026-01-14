import json
from datetime import datetime, timedelta
from database import EHRDatabase
from fitbit_api import FitbitAPI

class FitbitImporter:
    def __init__(self, db_path = "ehr.db"):
        self.db = EHRDatabase(db_path)
        self.api = FitbitAPI()
        
    #imports fitbit data to an existing patient 
    def import_to_patient(self, patient_id, fitbit_user_id, days = 30):
        print(f"importing {days} days of Fitbit data for patient {patient_id}")
        
        #calculating date range
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days = days-1)).strftime(("%Y-%m-%d"))
        
        try:
            steps_data = self.api.get_steps