# mini_api.py - Production-ready AAPL Stock Data API

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from datetime import date
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

# Safety check - fail fast if credentials missing
required_env_vars = ['DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME']
if not all(os.getenv(var) for var in required_env_vars):
    raise ValueError("❌ Missing required DB environment variables")

app = FastAPI(title="AAPL Stock Data API")

# Development CORS - change to specific domains in production
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"], 
    allow_credentials=True,
    allow_methods=["GET"], 
    allow_headers=["*"]
)

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'), 
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'port': 3306,
    'use_pure': True,
    'use_unicode': True,
    'charset': 'utf8mb4',
    'autocommit': False
}

@app.get("/")
async def get_stock_data(
    start_date: date = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: date = Query(None, description="End date (YYYY-MM-DD)"),
    limit: int = Query(50, ge=1, le=1000, description="Max records")
):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # Build dynamic query based on date range
        base_query = "SELECT DISTINCT date, CAST(close AS SIGNED INTEGER) as close FROM apple_stock WHERE close IS NOT NULL"
        params = []

        if start_date:
            base_query += " AND date >= %s"
            params.append(start_date)

        if end_date:
            base_query += " AND date <= %s"
            params.append(end_date)

        base_query += " ORDER BY date DESC LIMIT %s"
        params.append(limit)

        cursor.execute(base_query, params)
        raw_results = cursor.fetchall()
        
        data = [{"date": r["date"], "close": r["close"]} for r in raw_results]
        labels = [str(d['date']) for d in data]
        values = [float(d['close']) for d in data]
        
        # Date range summary
        date_summary = f"Date range: {start_date or 'earliest'} to {end_date or 'latest'} (showing {len(data)} records)"
        
        cursor.close()
        
    except Exception as e:
        data = []
        labels = []
        values = []
        date_summary = "No data available"
    
    finally:
        if conn and conn.is_connected():
            conn.close()

    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>🍎 AAPL Stock Data</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }}
            .controls {{ background: #f5f5f5; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
            input[type="date"] {{ padding: 8px; margin: 0 10px; }}
            input[type="number"] {{ padding: 8px; margin: 0 10px; width: 80px; }}
            button {{ padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; margin: 0 5px; }}
            button:hover {{ background: #0056b3; }}
            canvas {{ max-height: 500px; width: 100%; }}
            .summary {{ color: #666; font-size: 14px; margin-top: 10px; }}
        </style>
    </head>
    <body>
        <h1>🍎 AAPL Stock Data API</h1>
        
        <div class="controls">
            <form id="dateForm" method="GET">
                <label>Start Date:</label>
                <input type="date" name="start_date" value="{start_date or ''}">
                
                <label>End Date:</label>
                <input type="date" name="end_date" value="{end_date or ''}">
                
                <label>Max Records:</label>
                <input type="number" name="limit" value="{limit}" min="1" max="1000">
                
                <button type="submit">Update Chart</button>
                <button type="button" onclick="resetForm()">Reset</button>
            </form>
            <div class="summary">{date_summary}</div>
        </div>
        
        <canvas id="chart"></canvas>
        
        <script>
            const ctx = document.getElementById('chart').getContext('2d');
            new Chart(ctx, {{
                type: 'line',
                data: {{ 
                    labels: {labels!r}, 
                    datasets:[{{ 
                        label: 'AAPL Close Price',
                        data: {values!r}, 
                        borderColor: 'rgb(75, 192, 192)',
                        backgroundColor: 'rgba(75, 192, 192, 0.1)',
                        tension: 0.1,
                        fill: true
                    }}] 
                }},
                options: {{ 
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{ 
                        y: {{ beginAtZero: false }} 
                    }}
                }}
            }});
            
            function resetForm() {{
                document.querySelector('[name="start_date"]').value = '';
                document.querySelector('[name="end_date"]').value = '';
                document.querySelector('[name="limit"]').value = '50';
                document.getElementById('dateForm').submit();
            }}
        </script>
    </body>
    </html>
    """)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
