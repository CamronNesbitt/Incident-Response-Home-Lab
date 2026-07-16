import os
import time
from flask import Flask, jsonify, render_template_string
import psycopg2
from psycopg2 import OperationalError

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "db")
DB_NAME = os.environ.get("DB_NAME", "lumen")
DB_USER = os.environ.get("DB_USER", "lumen_user")
DB_PASS = os.environ.get("DB_PASS", "lumen_pass")

PAGE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Lumen Analytics Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; background: #0f172a; color: #e2e8f0; padding: 40px; }
        .card { background: #1e293b; border-radius: 10px; padding: 24px; max-width: 500px; margin: auto; }
        h1 { color: #38bdf8; }
        .status-ok { color: #4ade80; font-weight: bold; }
        .status-error { color: #f87171; font-weight: bold; }
        table { width: 100%; margin-top: 20px; border-collapse: collapse; }
        td, th { padding: 8px; border-bottom: 1px solid #334155; text-align: left; }
    </style>
</head>
<body>
    <div class="card">
        <h1>📊 Lumen Analytics Dashboard</h1>
        <p>Database status: <span class="{{ status_class }}">{{ status }}</span></p>
        {{ content|safe }}
    </div>
</body>
</html>
"""

def get_connection():
    return psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS, connect_timeout=3
    )

@app.route("/")
def dashboard():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, metric_name, value FROM metrics ORDER BY id;")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        table_rows = "".join(
            f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>" for r in rows
        )
        content = f"""
        <table>
            <tr><th>ID</th><th>Metric</th><th>Value</th></tr>
            {table_rows}
        </table>
        """
        return render_template_string(
            PAGE_TEMPLATE, status="Connected", status_class="status-ok", content=content
        )
    except OperationalError as e:
        content = f"<p>Could not load metrics. Error detail: <code>{str(e)}</code></p>"
        return render_template_string(
            PAGE_TEMPLATE, status="Connection Failed", status_class="status-error", content=content
        ), 500

@app.route("/health")
def health():
    try:
        conn = get_connection()
        conn.close()
        return jsonify({"status": "healthy", "db": "reachable"}), 200
    except OperationalError as e:
        return jsonify({"status": "unhealthy", "db": "unreachable", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
