# scripts/process_data.py

def calculate_roi(data):
    """
    Calculate the ROI based on the provided data.
    Replace this logic with your actual ROI calculation.
    """
    # Example logic for ROI calculation
    total_cost = data.get("total_cost", 0)
    total_revenue = data.get("total_revenue", 0)
    
    if total_cost == 0:  # Avoid division by zero
        return 0
    
    roi = (total_revenue - total_cost) / total_cost * 100
    return roi

# Main script logic
import json

# Load data fetched by the GitHub Actions workflow
with open("data.json", "r") as file:
    data = json.load(file)

# Calculate ROI
roi = calculate_roi(data)

# Generate HTML
html_content = f"""
<!DOCTYPE html>
<html>
<head>
  <title>ROI Dashboard</title>
</head>
<body>
  <h1>ROI Dashboard</h1>
  <p>Total Cost: {data.get("total_cost", 0)}</p>
  <p>Total Revenue: {data.get("total_revenue", 0)}</p>
  <p>ROI: {roi:.2f}%</p>
</body>
</html>
"""

# Write the generated HTML to the public folder
import os
os.makedirs("public", exist_ok=True)
with open("public/index.html", "w") as file:
    file.write(html_content)
