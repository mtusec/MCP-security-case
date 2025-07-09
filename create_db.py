import sqlite3
import csv
import os

def create_and_populate_db():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CSV_PATH = os.path.join(BASE_DIR, "synthetic_medical_records.csv")
    DB_PATH = os.path.join(BASE_DIR, "medical_records.db")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medical_records (
            PatientID TEXT PRIMARY KEY,
            FirstName TEXT,
            LastName TEXT,
            Sex TEXT,
            DateOfBirth TEXT,
            Age INTEGER,
            EncounterDate TEXT,
            EncounterType TEXT,
            DiagnosisCode TEXT,
            DiagnosisDescription TEXT,
            Medications TEXT,
            Allergies TEXT,
            BP_Systolic INTEGER,
            BP_Diastolic INTEGER,
            HeartRate INTEGER,
            Notes TEXT
        )
    """)

    try:
        with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cursor.execute("""
                    INSERT OR REPLACE INTO medical_records (
                        PatientID, FirstName, LastName, Sex, DateOfBirth, Age,
                        EncounterDate, EncounterType, DiagnosisCode, DiagnosisDescription,
                        Medications, Allergies, BP_Systolic, BP_Diastolic, HeartRate, Notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    row['PatientID'], row['FirstName'], row['LastName'], row['Sex'], row['DateOfBirth'],
                    int(row['Age']), row['EncounterDate'], row['EncounterType'], row['DiagnosisCode'],
                    row['DiagnosisDescription'], row['Medications'], row['Allergies'],
                    int(row['BP_Systolic']), int(row['BP_Diastolic']), int(row['HeartRate']), row['Notes']
                ))
        print(f"Successfully imported {reader.line_num - 1} records from {CSV_PATH}")
    except FileNotFoundError:
        print(f"Error: CSV file not found at {CSV_PATH}")
    except Exception as e:
        print(f"Error importing CSV: {str(e)}")

    conn.commit()
    conn.close()
    print("Database created and populated with records.")

if __name__ == "__main__":
    create_and_populate_db()