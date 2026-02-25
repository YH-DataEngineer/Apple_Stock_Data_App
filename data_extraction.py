"""
Apple Stock Data Fetcher - Downloads 1 month of daily AAPL stock data from Yahoo Finance
Saves raw JSON response to apple_stock.json for further processing/transformation.
Handles Yahoo's bot detection with proper User-Agent header.
"""

import requests # HTTP client for making API requests to Yahoo Finance
import json # JSON encoder/decoder for parsing Yahoo's response and saving to file
from datetime import datetime
import os

def get_apple_stock():
    """
    Main function to fetch AAPL stock data from Yahoo Finance unofficial API.
    
    Returns:
        dict: Raw JSON response containing chart data, metadata, and timestamps
    """
    # Yahoo Finance chart API endpoint - unofficial but widely used
    # This URL provides OHLCV (Open/High/Low/Close/Volume) data

    url = "https://query1.finance.yahoo.com/v8/finance/chart/AAPL"
    
    # Query parameters defining data granularity and time range
    params = {
        "interval": "1d", # 1 day candles (vs 1m, 1h, 1wk, etc.)
        "range": "1mo"# 1 month of historical data (other options: 5d, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
    }
    
    
    # Headers REQUIRED by Yahoo - they block requests without User-Agent
    # Mimics a real Chrome browser to bypass bot detection
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    # DEBUG: Check what actually came back
    # === DEBUGGING SECTION === (Safe to keep - only shows HTTP metadata, not sensitive data)
    # Print status for troubleshooting connection issues (200 = success, 403 = blocked, 429 = rate limited)
    print(f"Status: {response.status_code}")
    print(f"Content-Type: {response.headers.get('content-type')}")
    print(f"First 200 chars: {response.text[:200]}")
    
    # Fix 1: Check status code
    # Make HTTP GET request with params and headers
    # requests.get() returns Response object with status_code, headers, text, etc.
    response.raise_for_status()
    
    # Fix 2: Check if response is JSON before parsing (Yahoo occasionally returns empty string)
    if not response.text.strip():
        raise ValueError("Empty response from Yahoo")
    
    # Parse JSON string into Python dict - Yahoo returns well-formed JSON
    data = response.json()

    # Navigate Yahoo's nested response structure: data["chart"]["result"] = array of symbol results (AAPL is index 0)
    # result[0] contains meta + timestamp + indicators data
    result = data["chart"]["result"][0]

    # Extract metadata (current price, timezone, market state, etc.)
    meta = result["meta"]


    # Write COMPLETE raw response to file (not just result/meta)
    # Overwrites file each run - add timestamp to filename if you want history
    # with open("apple_stock.json", "w") as f: json.dump(data, f, indent=4)'''
    

    # this code replace overwrite file for production -- Every run preserved , easy rollback, 
    

    # Generate filename: apple_stock_20260218_1528.json
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"apple_stock_{timestamp}.json"

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    
    # Success confirmation for user
    print("Saved successfully!")
    return filename


# Standard Python idiom - makes script executable when run directly running this seperately but in production not required as we are ruunning in tranformation layer 
if __name__ == "__main__":
    get_apple_stock()
