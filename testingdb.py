# test_simple_system.py
from database import EHRDatabase
from fitbit_api import FitbitAPI

# 1. Test database works
db = EHRDatabase("simple_ehr.db")

try:
    #EXPLANATION OF WORKFLOW HERE WOAH SO CONVENIENT TO DO IT HERE
    
    #STEP 1: CREATE A NEW PATIENT
    patient_id1 = db.add_patient("Arthur")
    print(f"Patient ID1: {patient_id1}")
    
    #testing step... GET DATA
    api = FitbitAPI()
    start = "2025-08-11"
    end = "2025-08-13"
    
    #getting data
    steps_data = api.get_steps(start, end)
    print(f"\nYour actual steps today: {steps_data}")
    
    #STEP 2: GET AND ADD DATA
    db.import_fitbit_data( patient_id1, start, end)
    
    #reading data -> exporting to a CSV
    count = db.export_patient_to_csv(patient_id1, "test_simple.csv")

except Exception as e:
    print(f"Fitbit test skipped: {e}")

db.close()