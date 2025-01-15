import json
import os

# Load API data
with open("data.json", "r") as file:
    data = json.load(file)

# Perform ROI calculations
roi = calculate_roi(data)  # Your custom ROI calculation function

# Generate an HTML file
html_content = f"""
<!DOCTYPE html>
<html>
<head>
  <title>ROI Dashboard</title>
  <script src="chart.js"></script>
</head>
<body>
  <h1>ROI Dashboard</h1>
  <div id="chart"></div>
  <script>
    const roiData = {roi};
    generateChart(roiData);  // Use your JS to visualize data
  </script>
</body>
</html>
"""

# Write to the public directory
os.makedirs("public", exist_ok=True)
with open("public/index.html", "w") as file:
    file.write(html_content)
