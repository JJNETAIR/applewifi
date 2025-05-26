import os
import shutil

def create_flask_app_files(base_dir):
    """
    Creates the directory structure and files for the Flask application.
    """
    templates_dir = os.path.join(base_dir, "templates")
    static_dir = os.path.join(base_dir, "static")

    os.makedirs(templates_dir, exist_ok=True)
    os.makedirs(static_dir, exist_ok=True)

    # Create app.py
    app_py = """from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# Dummy voucher data (for demonstration purposes)
# In a real application, this would be replaced with a database
vouchers = {
    "ABC123": {"start_date": "2025-05-01", "type": "15 days"},
    "XYZ789": {"start_date": "2025-05-10", "type": "30 days"}
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    code = request.form['code']
    info = vouchers.get(code.upper())
    if info:
        start_date = datetime.strptime(info["start_date"], "%Y-%m-%d")
        days = 15 if "15" in info["type"] else 30
        end_date = start_date + timedelta(days=days)
        remaining_days = (end_date - datetime.now()).days
        return render_template("result.html", code=code.upper(), valid=True, start=start_date.date(), end=end_date.date(), days=remaining_days)
    return render_template("result.html", code=code.upper(), valid=False)

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/add', methods=['POST'])
def add():
    code = request.form['code'].upper()
    start_date = request.form['start_date']
    duration = request.form['duration']
    vouchers[code] = {"start_date": start_date, "type": duration}
    return redirect(url_for('admin'))

if __name__ == '__main__':
    # Use environment variable for port in production
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
"""
    with open(os.path.join(base_dir, "app.py"), "w") as f:
        f.write(app_py)

    # HTML templates
    index_html = """<!DOCTYPE html>
<html>
<head>
    <title>APPLE WIFI - Voucher Check</title>
    <style>
        body { font-family: sans-serif; text-align: center; padding: 50px; font-size: 24px; }
        input, button { font-size: 24px; padding: 10px; margin: 10px; }
    </style>
</head>
<body>
    <h1>APPLE WIFI</h1>
    <p>Voucher Validity Check</p>
    <form action="/check" method="post">
        <input type="text" name="code" placeholder="Enter Voucher Code" required>
        <button type="submit">Check</button>
    </form>
</body>
</html>
"""
    with open(os.path.join(templates_dir, "index.html"), "w") as f:
        f.write(index_html)

    result_html = """<!DOCTYPE html>
<html>
<head>
    <title>Result - APPLE WIFI</title>
    <style>
        body { font-family: sans-serif; text-align: center; padding: 50px; font-size: 24px; }
        .valid { color: green; }
        .invalid { color: red; }
    </style>
</head>
<body>
    <h1>APPLE WIFI</h1>
    {% if valid %}
        <p class="valid">Voucher {{ code }} is Valid ✅</p>
        <p>Start Date: {{ start }}</p>
        <p>Valid Till: {{ end }}</p>
        <p>Remaining Days: {{ days }}</p>
    {% else %}
        <p class="invalid">Voucher {{ code }} is Invalid ❌</p>
    {% endif %}
    <a href="/">Back</a>
</body>
</html>
"""
    with open(os.path.join(templates_dir, "result.html"), "w") as f:
        f.write(result_html)

    admin_html = """<!DOCTYPE html>
<html>
<head>
    <title>Admin - APPLE WIFI</title>
    <style>
        body { font-family: sans-serif; text-align: center; padding: 50px; font-size: 24px; }
        input, select, button { font-size: 24px; padding: 10px; margin: 10px; }
    </style>
</head>
<body>
    <h1>Admin Panel - APPLE WIFI</h1>
    <form action="/add" method="post">
        <input type="text" name="code" placeholder="Voucher Code" required>
        <input type="date" name="start_date" required>
        <select name="duration">
            <option value="15 days">15 days</option>
            <option value="30 days">30 days</option>
        </select>
        <button type="submit">Add Voucher</button>
    </form>
</body>
</html>
"""
    with open(os.path.join(templates_dir, "admin.html"), "w") as f:
        f.write(admin_html)

    # Create requirements.txt
    with open(os.path.join(base_dir, "requirements.txt"), "w") as f:
        f.write("Flask\ngunicorn") # Add gunicorn for production server

    # Create a Procfile for Render.com
    # This tells Render how to run your application
    with open(os.path.join(base_dir, "Procfile"), "w") as f:
        f.write("web: gunicorn app:app")


# Define the base directory for the Flask app
base_directory = "apple_wifi_site"

# Clean up previous runs if any
if os.path.exists(base_directory):
    shutil.rmtree(base_directory)

# Create all files and directories
create_flask_app_files(base_directory)

print(f"Flask application structure created in '{base_directory}' with Procfile and gunicorn for deployment.")

