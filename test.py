import requests

data = {
    "Temperature": 24.4,
    "pH": 7.620,
    "Turbidity": 0.179,
    "DissolvedOxygen": 8.0,
    "Conductivity": 1215.85,
    "TotalDissolvedSolids": 0.54,
    "Nitrate": 5,
    "Phosphate": 0.05,
    "TotalColiforms": 1,
    "Ecoli": 0,
    "BOD": 0.5,
    "COD": 78.9,
    "Hardness": 263.2,
    "Alkalinity": 150,
    "Iron": 0.7427,
}

response = requests.post("http://localhost:8000/evaluate/", json=data)

if response.status_code == 200:
    result = response.json()
    print(result)
else:
    print(f"Error: {response.status_code} - {response.text}")
