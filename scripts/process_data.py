import os
import json

def calculate_roi(data):
    """
    Calculate the ROI based on the provided data.
    This is a placeholder; replace it with your actual calculation logic.
    """
    total_cost = data.get("total_cost", 0)
    total_revenue = data.get("total_revenue", 0)
    if total_cost == 0:
        return 0  # Avoid division by zero
    return (total_revenue - total_cost) / total_cost * 100

def generate_dashboard(data, roi):
    """
    Generate the dashboard HTML, CSS, and JavaScript files.
    """
    # Create the public directory if it doesn't exist
    os.makedirs("public", exist_ok=True)

    # Write the HTML file
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ROI Dashboard</title>
        <link rel="stylesheet" href="style.css">
        <script src="script.js"></script>
    </head>
    <body>
        <h1>ROI Dashboard</h1>
        <div class="chart-container">
            <canvas id="roiChart"></canvas>
        </div>
        <p>Total Cost: ${data.get("total_cost", 0)}</p>
        <p>Total Revenue: ${data.get("total_revenue", 0)}</p>
        <p>ROI: {roi:.2f}%</p>
    </body>
    </html>
    """
    with open("public/index.html", "w") as file:
        file.write(html_content)

    # Write the CSS file
    css_content = """
    body {
        font-family: Arial, sans-serif;
        background-color: #f4f4f9;
        margin: 0;
        padding: 0;
    }
    h1 {
        text-align: center;
        padding: 20px;
    }
    .chart-container {
        width: 80%;
        margin: auto;
        padding: 20px;
        background: white;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    """
    with open("public/style.css", "w") as file:
        file.write(css_content)

    # Write the JavaScript file
    js_content = """
    const ctx = document.getElementById('roiChart').getContext('2d');
    const roiData = {
        labels: ['Q1', 'Q2', 'Q3', 'Q4'], // Replace with actual labels if needed
        datasets: [{
            label: 'ROI (%)',
            data: [10, 20, 30, 40], // Replace with actual data if needed
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }]
    };
    const config = {
        type: 'bar', // You can also use 'line', 'pie', etc.
        data: roiData,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
            }
        }
    };
    new Chart(ctx, config);
    """
    with open("public/script.js", "w") as file:
        file.write(js_content)

# Main logic
try:
    # Load the data file (replace with your actual data source)
    with open("data.json", "r") as file:
        data = json.load(file)

    # Calculate ROI
    roi = calculate_roi(data)

    # Generate dashboard files
    generate_dashboard(data, roi)

    print("Dashboard generated successfully in the public/ directory.")

except FileNotFoundError as e:
    print(f"Error: {e}. Ensure data.json exists.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
