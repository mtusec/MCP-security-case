import requests

req_url = "http://127.0.0.1:6278/mcp/"
req_headers = {"Accept-Encoding": "gzip, deflate, br", "Connection": "keep-alive", "User-Agent": "python-httpx/0.28.1", "Accept": "application/json, text/event-stream", "content-type": "application/json", }
req_json={"id": 0, "jsonrpc": "2.0", "method": "initialize", "params": {"capabilities": {"roots": {"listChanged": True}, "sampling": {}}, "clientInfo": {"name": "mcp", "version": "0.1.0"}, "protocolVersion": "2025-03-26"}}
res1 = requests.post(req_url, headers=req_headers, json=req_json)

print(res1.headers)
print(res1.text)
mcp_id = res1.headers["mcp-session-id"]
print(mcp_id)

req_headers["mcp-session-id"] =  mcp_id
print(req_headers)
req_json={"jsonrpc": "2.0", "method": "notifications/initialized"}
res2 = requests.post(req_url, headers=req_headers, json=req_json)
print("----------------------------------------------------------------------------------------")
print(res2.headers)
print(res2.text)


req_json={"id": 1, "jsonrpc": "2.0", "method": "resources/read", "params": {"uri": "resource://medical_record/P1001"}}
res3 = requests.post(req_url, headers=req_headers, json=req_json)
print("----------------------------------------------------------------------------------------")
print(res3.headers)
print(res3.text)

req_json={"id": 2, "jsonrpc": "2.0", "method": "prompts/get", "params": {"arguments": {"message": "{\n  \"PatientID\": \"P1000\",\n  \"FirstName\": \"Jennifer\",\n  \"LastName\": \"Williams\",\n  \"Sex\": \"M\",\n  \"DateOfBirth\": \"1977-08-20\",\n  \"Age\": 47,\n  \"EncounterDate\": \"2025-04-06\",\n  \"EncounterType\": \"Annual Checkup\",\n  \"DiagnosisCode\": \"J06.9\",\n  \"DiagnosisDescription\": \"Acute upper respiratory infection, unspecified\",\n  \"Medications\": \"Metformin 500\xe2\x80\xafmg, Amoxicillin 500\xe2\x80\xafmg, Albuterol Inhaler\",\n  \"Allergies\": \"Latex\",\n  \"BP_Systolic\": 113,\n  \"BP_Diastolic\": 67,\n  \"HeartRate\": 67,\n  \"Notes\": \"Patient advised to reduce sodium intake.\"\n}"}, "name": "get_prompt"}}
res4 = requests.post(req_url, headers=req_headers, json=req_json)
print("----------------------------------------------------------------------------------------")
print(res4.headers)
print(res4.text)

res5 = requests.delete(req_url, headers=req_headers)
print("----------------------------------------------------------------------------------------")
print(res5.headers)
print(res5.text)