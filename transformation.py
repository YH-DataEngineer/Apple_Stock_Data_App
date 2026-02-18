import mysql.connector
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file FIRST

# Safety check - fail fast if credentials missing
required_env_vars = ['DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME']
if not all(os.getenv(var) for var in required_env_vars):
    raise ValueError("❌ Missing required DB environment variables")

# transform data 
# load to mysql 
# FIXED: Ensure env vars exist
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'), 
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'port': 3306,
    'use_pure': True,
    'use_unicode': True,
    'charset': 'utf8mb4',
    'autocommit': False  # Explicitly disable autocommit
}

def connect_to_existing_db():
    """Connect + validate table structure"""
    
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Check table exists
    cursor.execute("SHOW TABLES LIKE 'apple_stock'")
    if not cursor.fetchone():
        raise ValueError("❌ Table 'apple_stock' does not exist!")
    
    # Get exact column names + types
    cursor.execute("DESCRIBE apple_stock")
    columns = {row[0]: row[1] for row in cursor.fetchall()}
    print("✅ Table columns:", columns)
    
    return conn, cursor, columns

def transform_json_to_relational(json_data):
    """Transform JSON → rows (your code is fine)"""
    result = json_data["chart"]["result"][0]
    meta = result["meta"]
    
    timestamps = result["timestamp"]
    ohlcv = result["indicators"]["quote"][0]
    
    rows = []
    for i, ts in enumerate(timestamps):
        row = {
            'timestamp': ts,
            'date': datetime.fromtimestamp(ts).strftime('%Y-%m-%d'),
            'open': ohlcv['open'][i] if i < len(ohlcv['open']) else None,
            'high': ohlcv['high'][i] if i < len(ohlcv['high']) else None,
            'low': ohlcv['low'][i] if i < len(ohlcv['low']) else None,
            'close': ohlcv['close'][i] if i < len(ohlcv['close']) else None,
            'volume': int(ohlcv['volume'][i]) if i < len(ohlcv['volume']) and ohlcv['volume'][i] else 0,
            'symbol': meta.get('symbol', 'AAPL'),
            'currency': meta.get('currency', 'USD'),
            'previous_close': meta.get('previousClose')
        }
        
        rows.append(row)
    
    return rows

def append_to_existing_table(conn, cursor, rows, columns):
    """Safe upsert with exact column matching"""
    # Build columns list from ACTUAL table
    insert_cols = ['timestamp', 'date', 'open', 'high', 'low', 'close', 'volume']
    if 'symbol' in columns: insert_cols.append('symbol')
    if 'currency' in columns: insert_cols.append('currency')
    if 'previous_close' in columns: insert_cols.append('previous_close')
    
    placeholders = ', '.join(['%s'] * len(insert_cols))
    insert_cols_str = ', '.join(insert_cols)
    
    query = f"""
        INSERT INTO apple_stock ({insert_cols_str})
        VALUES ({placeholders})
        ON DUPLICATE KEY UPDATE
            open=VALUES(open), high=VALUES(high), low=VALUES(low), 
            close=VALUES(close), volume=VALUES(volume)
    """
    
    # Match data to columns exactly
    data_tuples = []
    for r in rows:
        data = [r.get(col) for col in insert_cols]
        data_tuples.append(tuple(data))
    
    print(f"🔍 Executing query with {len(data_tuples)} rows...")
   
    
    cursor.executemany(query, data_tuples)
    conn.commit()  # CRITICAL: This was missing or failing!
    
    print(f"✅ Committed {cursor.rowcount} row(s)")

if __name__ == "__main__":
    conn = cursor = None
    
    try:
        # 1. Connect + validate
        conn, cursor, columns = connect_to_existing_db()
        
        # 2. Load JSON
        with open("apple_stock.json", "r") as f:
            json_data = json.load(f)
        
        rows = transform_json_to_relational(json_data)
        print(f"✅ Transformed {len(rows)} rows")
        
        # 3. Insert
        append_to_existing_table(conn, cursor, rows, columns)
        
        # 4. Verify
        cursor.execute("SELECT COUNT(*) FROM apple_stock")
        total = cursor.fetchone()[0]
        cursor.execute("SELECT date, close FROM apple_stock ORDER BY date DESC LIMIT 5")
        recent = cursor.fetchall()
        print(f"✅ Total rows: {total}")
        print("Recent data:", recent)
        
    except mysql.connector.Error as e:
        print(f"❌ MySQL Error {e.errno}: {e}")
    except FileNotFoundError:
        print("❌ apple_stock.json not found!")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            print("✅ Connection closed")
