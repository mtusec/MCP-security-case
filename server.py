import sqlite3
import subprocess

from mcp.server.fastmcp import FastMCP
import os
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "medical_records.db")

mcp = FastMCP(
    name="demo-server",
    host="0.0.0.0",
    port=6278,
)

logging.info("Starting VULNERABLE MCP server...")

@mcp.resource("resource://medical_record/{patient_id}")
def get_medical_record(patient_id: str) -> dict:
    """Retrieve a single patient record by PatientID."""
    logging.debug(f"Fetching medical record for PatientID: {patient_id}")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM medical_records WHERE PatientID = ?", (patient_id,))
        record = cursor.fetchone()
        conn.close()
        if record:
            columns = [desc[0] for desc in cursor.description]
            data = dict(zip(columns, record))
            logging.debug(f"Record found: {data}")
            return data
        logging.warning(f"Record not found for PatientID: {patient_id}")
        return {"error": "Record not found"}
    except Exception as e:
        logging.error(f"Database error for PatientID {patient_id}: {str(e)}")
        return {"error": f"Database error: {str(e)}"}

@mcp.tool()
def query_by_column(patient_id: str, order_by: str = "EncounterDate", descending: bool = False) -> dict:
    """
    Retrieve medical records for a patient, ordered by a specific field.
    """
    logging.debug(f"Fetching records for PatientID: {patient_id}, ordered by: {order_by}, desc: {descending}")
    try:
        direction = "DESC" if descending else "ASC"
        # VULNERABILITY: User input is directly formatted into the SQL query.
        sql = f"SELECT * FROM medical_records WHERE PatientID = {patient_id} ORDER BY {order_by} {direction}"
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        conn.close()
        if not records:
            logging.warning(f"No records found for PatientID: {patient_id}")
            return {"error": "No records found"}

        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in records]

        logging.debug(f"{len(result)} records found")
        return {"records": result}

    except Exception as e:
        logging.error(f"Database error: {str(e)}")
        return {"error": f"Database error: {str(e)}"}

@mcp.tool()
def insert_medical_record(
    PatientID: str,
    FirstName: str,
    LastName: str,
    Sex: str,
    DateOfBirth: str,
    Age: int,
    EncounterDate: str,
    EncounterType: str,
    DiagnosisCode: str,
    DiagnosisDescription: str,
    Medications: str,
    Allergies: str,
    BP_Systolic: int,
    BP_Diastolic: int,
    HeartRate: int,
    Notes: str
) -> str:
    """
    Insert or replace a medical record into the SQLite database.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO medical_records (
                PatientID, FirstName, LastName, Sex, DateOfBirth, Age,
                EncounterDate, EncounterType, DiagnosisCode, DiagnosisDescription,
                Medications, Allergies, BP_Systolic, BP_Diastolic, HeartRate, Notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            PatientID, FirstName, LastName, Sex, DateOfBirth, Age,
            EncounterDate, EncounterType, DiagnosisCode, DiagnosisDescription,
            Medications, Allergies, BP_Systolic, BP_Diastolic, HeartRate, Notes
        ))
        conn.commit()
        conn.close()
        logging.info(f"Inserted record for PatientID: {PatientID}")
        return f"Record inserted for PatientID: {PatientID}"
    except Exception as e:
        logging.error(f"Error inserting record: {str(e)}")
        return f"Error inserting record: {str(e)}"

@mcp.tool()
def export_medical_record(PatientID: str, output_file: str) -> str:
    """
    Export the specified patient's medical record to a CSV file.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM medical_records WHERE PatientID = ?", (PatientID,))
        record = cursor.fetchone()
        conn.close()
        if not record:
            return f"No record found for PatientID: {PatientID}"

        values = [str(v) for v in record]

        csv_line = ",".join(values)

        output_file = f"export_{output_file}.csv"
        shell_cmd = f"echo '{csv_line}' > {output_file}"  # injection happens here

        subprocess.call(shell_cmd, shell=True)  # command injection point

        return f"Exported to: {output_file}"

    except Exception as e:
        logging.error(f"Error exporting record: {str(e)}")
        return f"Error exporting record: {str(e)}"

@mcp.tool()
def update_medical_record(PatientID: str, updates: dict) -> str:
    """
    Update specific fields in a medical record given a PatientID.
    """
    try:
        if not updates:
            return "No fields provided for update."
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        set_clause = ", ".join([f"{key} = ?" for key in updates.keys()])
        values = list(updates.values()) + [PatientID]

        sql = f"UPDATE medical_records SET {set_clause} WHERE PatientID = ?"
        logging.info(f"Executing SQL: {sql} with values {values}")
        cursor.execute(sql, values)
        conn.commit()
        conn.close()
        if cursor.rowcount == 0:
            return f"No record found for PatientID: {PatientID}"
        return f"Record updated for PatientID: {PatientID}"

    except Exception as e:
        return f"Error updating record: {str(e)}"

@mcp.tool()
def delete_medical_record(PatientID: str) -> str:
    """
    Delete a medical record from the database by PatientID.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM medical_records WHERE PatientID = ?", (PatientID,))
        conn.commit()
        deleted = cursor.rowcount
        conn.close()

        if deleted == 0:
            return f"No record found for PatientID: {PatientID}"
        return f"Record deleted for PatientID: {PatientID}"
    except Exception as e:
        logging.error(f"Error deleting record: {str(e)}")
        return f"Error deleting record: {str(e)}"



@mcp.prompt()
def get_prompt(message: str) -> str:
    prompt = f"Analyze the risk of heart attack for this patient based on the following data: {message}. Return only 'Risk: X%' where X is a number."
    return prompt

@mcp.tool()
def calculate_average_risk(responses: list) -> float:
    """Calculate the average of risk rates from responses"""
    logging.debug(f"Calculating average risk for responses: {responses}")
    import re
    risk_rates = []
    for response in responses:
        match = re.search(r"Risk: (\d+)%", response)
        if match:
            risk_rates.append(int(match.group(1)))
        else:
            logging.error(f"Could not parse risk from response: {response}")
    avg = sum(risk_rates) / len(risk_rates) if risk_rates else 0.0
    logging.debug(f"Average risk calculated: {avg}")
    return avg

if __name__ == "__main__":
    logging.info("Starting MCP server")
    mcp.run(transport="streamable-http")