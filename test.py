import requests

data = {
    "Temperature": 24.4,
    "pH": 7.620,
    "Turbidity": 0.179,  # Assuming NTU
    "DissolvedOxygen": 8.0,  # Example value - REPLACE with your actual DO measurement
    "Conductivity": 1215.85,
    "TotalDissolvedSolids": 0.54, # in g/L
    "Nitrate": 5,  # Example value - add if you have data
    "Phosphate": 0.05,  # Example value - add if you have data
    "TotalColiforms": 1,  # Example value - add if you have data
    "Ecoli": 0,  # Example value - add if you have data
    "BOD": 0.5,
    "COD": 78.9,
    "Hardness": 263.2,  # Added
    "Alkalinity": 150, # Example value
    "Iron": 0.7427,  # Added, converted to mg/L
}

response = requests.post("http://localhost:8000/evaluate/", json=data)

if response.status_code == 200:
    result = response.json()
    print(result)
else:
    print(f"Error: {response.status_code} - {response.text}")
