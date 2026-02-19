
# Apple_Stock_Data_App

Dockerized FastAPI app that fetches real-time Apple stock data, processes it through an ETL pipeline into MySQL, and serves interactive graph endpoints. Users query date ranges via Swagger UI to visualize stock trends with **zero local setup**!

[![Docker Ready](https://img.shields.io/badge/Docker-Ready-blue)](https://hub.docker.com/) [![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen)](https://github.com/DataEngineer/Apple_Stock_Data_App/actions)

## ✨ Features
- 🎯 Real-time AAPL stock data fetching
- 🔄 ETL pipeline (Extract → Transform → Load) to MySQL
- 📊 FastAPI endpoints with date-range filtering
- 📈 Interactive graphs via web interface
- 🚀 One-command Docker deployment

## 🏗️ Architecture

- **Data Source Layer** – External stock market API providing raw AAPL price and volume data  
- **Ingestion & ETL Layer** – Python ETL jobs extract JSON data, transform it (cleaning, type casting, feature columns), and load it into the MySQL database  
- **Database Layer (MySQL)** – Stores historical AAPL stock data in a structured schema optimized for time‑series and date‑range queries  
- **API Layer (FastAPI)** – Exposes REST endpoints for querying stock data by date range and other filters, returning JSON responses consumed by the frontend or tools  
- **Visualization Layer** – Uses API responses to render interactive graphs so users can explore stock trends visually  
- **Containerization Layer (Docker)** – Packages the FastAPI app (and optional ETL tooling) into a Docker image for consistent, portable deployment with a single run command  


## 📋 Prerequisites
| Requirement | Details |
|-------------|---------|
| **Docker** | Desktop (Win/Mac) or Engine (Linux) |
| **Port** | 8000 free locally |
| **Git** | For cloning |


## 🔧 MySQL Setup (External - You Provide)

**Your own MySQL server required** (Local/Cloud):
## 🗄️ MySQL Setup (REQUIRED - External)

**Your own MySQL server needed** (Local/Cloud like AWS ,AZURE, GCP):

### 1. Create Database + Table
```sql
CREATE DATABASE aapl_stocks;
USE aapl_stocks;

CREATE TABLE stock_data (
    timestamp BIGINT PRIMARY KEY,
    date DATE,
    open DECIMAL(10,4),
    high DECIMAL(10,4),
    low DECIMAL(10,4),
    close DECIMAL(10,4),
    volume BIGINT,
    symbol VARCHAR(10),
    currency VARCHAR(3),
    previous_close DECIMAL(10,4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

### **2. Configure Connection.env file:**

In the app folder create `.env` file in project root:

```bash
# .env (create + edit passwords)
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_secure_password
MYSQL_DATABASE=aapl_stocks
MYSQL_ROOT_PASSWORD=your_secure_password
```


**Quick setup:**
```bash
cp .env.example .env
# Edit passwords in .env
docker run --env-file .env -p 8000:8000 apple-stock-api
```

**Defaults:** `MYSQL_PASSWORD=admin123`

## 🚀 Quick Start (2 Minutes)
```bash
git clone https://github.com/DataEngineer/Apple_Stock_Data_App.git
cd Apple_Stock_Data_App
cp .env.example .env  # Edit passwords
docker build -t apple-stock-api .
docker run --env-file .env -p 8000:8000 apple-stock-api
```

✅ **Open:** [http://localhost:8000/docs](http://localhost:8000/docs)

## 🎮 API Usage
```
1. Visit http://localhost:8000/docs (Swagger UI)
2. Query: /stocks?start_date=2025-01-01&end_date=2025-02-18
3. View interactive stock graphs!
```

## 🌐 Access URLs
| ✅ **Works** | ❌ **Fails** | **Reason** |
|-------------|--------------|------------|
| `localhost:8000` | `0.0.0.0:8000` | Docker binding only |
| `127.0.0.1:8000` | | Both reach container |

## 🐳 Docker Flow
```
GitHub Repo + .env
      ↓ clone
Docker Build → Image (FastAPI + MySQL + ETL)
      ↓ docker run
Container → localhost:8000 ✅
```

## 🔧 Troubleshooting
| **Problem** | **Fix** |
|-------------|---------|
| Port 8000 busy | `docker run -p 8080:8000` → `localhost:8080` |
| `0.0.0.0` fails | Use `localhost:8000` |
| MySQL fails | Check `.env` passwords |
| No response | `docker logs <container-id>` |
| Build fails | `docker image prune` |

## 🛠️ Local Dev (Optional)
```bash
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

## 📁 Structure
```
├── test/                 # pytest suite ✅
├── Dockerfile           # Container magic
├── .env.example         # MySQL template
├── main.py             # FastAPI endpoints
├── etl_pipeline.py     # Stock → MySQL
└── requirements.txt
```

## 🤝 Contributing
1. Fork repo
2. `git checkout -b feature/new-stock`
3. Commit + PR

## 📄 License
MIT - Free for learning/work!

## 👨‍💼 Demo Script
**3-min flow:** Clone → `.env` → Docker → `/docs` → Graph appears!


