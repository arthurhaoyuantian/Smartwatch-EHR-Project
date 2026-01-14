import sqlite3
from datetime import datetime, timedelta

class EHRDatabase:
    #constructor -> connects app to database file and creates the tables
    def __init__(self, db_path = "ehr.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
        
    #creates tables
    def create_tables(self):
        #patients table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                fitbit_user_id TEXT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
                
            )
        ''')
        
        #health data table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS health_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER,
                date TEXT,
                steps INTEGER,
                heart_rate_avg INTEGER,
                heart_rate_min INTEGER,
                heart_rate_max INTEGER,
                sleep_duration REAL,
                source TEXT,
                imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
                UNIQUE (patient_id, date, source)
            )
        ''')
        
        #save changes
        self.conn.commit()
        
        
    #CRUD methods 
    
    #adds a patient to table
    def add_patient(self, name, fitbit_user_id = None):
        try:
            cursor = self.conn.execute(
                'INSERT INTO patients (name, fitbit_user_id) VALUES (?, ?)',
                (name, fitbit_user_id)
            )
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
        
    #returns all patients as a list of tuples
    def get_all_patients(self):
        cursor = self.conn.execute('SELECT patient_id, name FROM patients ORDER BY name')
        return cursor.fetchall()
    
    #returns individual patient as a tuple 
    def get_patient_by_id(self, patient_id):
        cursor = self.conn.execute(
            'SELECT patient_id, name, fitbit_user_id FROM patients WHERE patient_id = ?',
            (patient_id,)
        )
        return cursor.fetchone()
    
    #adds the daily health metrics for a patient 
    def add_health_data(self, patient_id, date, steps = None, heart_rate_avg = None, 
                        heart_rate_min = None, heart_rate_max = None, sleep_duration = None,
                        source = 'fitbit'):
        try:
            self.conn.execute('''
                INSERT INTO health_metrics (
                    patient_id, date, steps, heart_rate_avg, heart_rate_min, 
                    heart_rate_max, sleep_duration, source) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (patient_id, date, steps, heart_rate_avg, heart_rate_min, 
                    heart_rate_max, sleep_duration, source)
            )
            
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    #returns the health metrics of a patient, filtered by date range if included
    def get_patient_health_data(self, patient_id, start_date = None, end_date = None):
        query = '''
            SELECT date, steps, heart_rate_avg, heart_rate_min, 
            heart_rate_max, sleep_duration, source FROM health_metrics 
            WHERE patient_id = ?
        '''
        params = [patient_id]
        
        if start_date:
            query += ' AND date >= ?'
            params.append(start_date)
        if end_date:
            query += ' AND date <= ?'
            params.append(end_date)
        
        query += 'ORDER BY date'
        
        cursor = self.conn.execute(query, params)
        return cursor.fetchall() #return all data that matches these params specific to this patient
    
    #adds this patient to the csv file on storage 
    def export_patient_to_csv(self, patient_id, filename):
        import csv
        
        data = self.get_patient_health_data(patient_id)
        
        with open(filename, 'w', newline = '') as my_file:
            writer = csv.writer(my_file)
            writer.writerow(['date', 'steps', 'hr_avg', 'hr_min', 'hr_max', 'sleep', 'source'])
            writer.writerows(data)
            
        return len(data)
            
    #closes database connection 
    def close(self):
        self.conn.close()