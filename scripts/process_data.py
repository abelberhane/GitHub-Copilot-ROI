import os
import requests
import json

API_URL = "https://api.github.com/orgs/SullyDevSquad/copilot/usage" # Update the orgs section with your own 
ORG = "SullyDevSquad" 

def fetch_data():
    token = os.getenv("GITHUB_API_TOKEN")
    if not token:
        raise Exception("GITHUB_API_TOKEN environment variable is not set.")
    
    headers = {"Authorization": f"token {token}"}
    response = requests.get(API_URL.format(org=ORG), headers=headers)

    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list):
            return data[0] if data else {}
        return data
    else:
        raise Exception(f"Failed to fetch data: {response.status_code} {response.text}")

def calculate_metrics(data):
    suggested_lines = data.get("total_lines_suggested", 0)
    accepted_lines = data.get("total_lines_accepted", 0)
    total_users = data.get("total_active_users", 0)
    active_chat_users = data.get("total_active_chat_users", 0)
    dau = [day.get("total_active_users", 0) for day in data.get("breakdown", [])]

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
    os.makedirs("public", exist_ok=True)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Avengers Dashboard</title>
        <link rel="stylesheet" href="style.css">
        <script src="script.js"></script>
    </head>
    <body>
        <header>
            <div class="header-content">
                <img src="logo.png" alt="SHIELD Logo" class="logo">
                <h1>Avengers Dashboard</h1>
            </div>
        </header>
        <main>
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
        </main>
    </body>
    </html>
    """
    with open("public/index.html", "w") as file:
        file.write(html_content)

try:
    data = fetch_data()
    metrics = calculate_metrics(data)
    generate_dashboard(metrics)
    print("Dashboard generated successfully in the public/ directory.")
except Exception as e:
    print(f"Error: {e}")

