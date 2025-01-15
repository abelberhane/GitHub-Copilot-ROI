import os
import json
import requests

# GitHub API endpoint and organization
API_URL = "https://api.github.com/orgs/SullyDevSquad/copilot/usage" # Update the orgs section with your own 
ORG = "SullyDevSquad"                                               # Update your organization name here

def fetch_data():
    """
    Fetch Copilot usage data from the GitHub API using an environment variable for the token.
    """
    token = os.getenv("GITHUB_API_TOKEN")
    if not token:
        raise Exception("GITHUB_API_TOKEN environment variable is not set.")
    
    headers = {"Authorization": f"token {token}"}
    response = requests.get(API_URL.format(org=ORG), headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code} {response.text}")

def calculate_metrics(data):
    """
    Calculate key metrics for the dashboard.
    """
    suggested_lines = data.get("suggested_lines", 0)
    accepted_lines = data.get("accepted_lines", 0)
    total_users = data.get("total_users", 0)
    dau = data.get("dau", [])
    active_chat_users = data.get("total_active_chat_users", 0)

    acceptance_rate = (accepted_lines / suggested_lines) * 100 if suggested_lines else 0
    adoption_rate = (sum(dau) / total_users) * 100 if total_users else 0
    average_lines_accepted = accepted_lines / total_users if total_users else 0

    return {
        "suggested_lines": suggested_lines,
        "accepted_lines": accepted_lines,
        "acceptance_rate": acceptance_rate,
        "dau": dau,
        "active_chat_users": active_chat_users,
        "adoption_rate": adoption_rate,
        "average_lines_accepted": average_lines_accepted,
        "total_users": total_users,
    }

def generate_dashboard(metrics):
    """
    Generate the dashboard HTML, CSS, and JavaScript files.
    """
    os.makedirs("public", exist_ok=True)

    # HTML with sections for metrics
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GitHub Copilot ROI Dashboard</title>
        <link rel="stylesheet" href="style.css">
        <script src="script.js"></script>
    </head>
    <body>
        <header>
            <img src="logo.png" alt="Company Logo" class="logo">
            <h1>GitHub Copilot ROI Dashboard</h1>
        </header>
        <section id="acceptance-rate">
            <h2>Acceptance Rate</h2>
            <p>Suggested Lines: {metrics['suggested_lines']}</p>
            <p>Accepted Lines: {metrics['accepted_lines']}</p>
            <p>Acceptance Rate: {metrics['acceptance_rate']:.2f}%</p>
        </section>
        <section id="usage-growth">
            <h2>Usage Growth</h2>
            <p>Total Active Chat Users: {metrics['active_chat_users']}</p>
            <canvas id="dauChart"></canvas>
        </section>
        <section id="additional-metrics">
            <h2>Additional Metrics</h2>
            <p>Total Users: {metrics['total_users']}</p>
            <p>Adoption Rate: {metrics['adoption_rate']:.2f}%</p>
            <p>Average Lines Accepted per User: {metrics['average_lines_accepted']:.2f}</p>
        </section>
    </body>
    </html>
    """
    with open("public/index.html", "w") as file:
        file.write(html_content)

    # Write CSS
    css_content = """
    body {
        font-family: Arial, sans-serif;
        background-color: #f4f4f9;
        margin: 0;
        padding: 0;
    }
    header {
        text-align: center;
        padding: 20px;
    }
    .logo {
        max-width: 150px;
    }
    section {
        margin: 20px;
        padding: 20px;
        background: white;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    """
    with open("public/style.css", "w") as file:
        file.write(css_content)

    # Write JavaScript for DAU Chart
    js_content = f"""
    const ctx = document.getElementById('dauChart').getContext('2d');
    const dauData = {{
        labels: [...Array({len(metrics['dau'])}).keys()].map(i => `Day ${i + 1}`),
        datasets: [{{
            label: 'Daily Active Users',
            data: {metrics['dau']},
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }}]
    }};
    const config = {{
        type: 'line',
        data: dauData,
        options: {{
            responsive: true,
            plugins: {{
                legend: {{
                    position: 'top',
                }},
            }}
        }}
    }};
    new Chart(ctx, config);
    """
    with open("public/script.js", "w") as file:
        file.write(js_content)

# Main logic
try:
    data = fetch_data()
    metrics = calculate_metrics(data)
    generate_dashboard(metrics)
    print("Dashboard generated successfully in the public/ directory.")
except Exception as e:
    print(f"Error: {e}")
