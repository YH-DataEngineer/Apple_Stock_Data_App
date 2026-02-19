# Apple Stock Data App

Dockerized **FastAPI app** that fetches real-time **Apple (AAPL) stock data**, processes it through an **ETL pipeline** into **MySQL**, and serves **interactive graph endpoints**. Users query date ranges via **Swagger UI** to visualize stock trends with **zero local setup**!

[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-Push%20Success-blue)](https://hub.docker.com/) [![GitHub Actions](https://img.shields.io/badge/CI%20/CD-Passing-brightgreen)](https://github.com/YH-DataEngineer/Apple_Stock_Data_App/actions)

## ✨ Features

- 🎯 **Real-time AAPL stock data** fetching from free APIs
- 🔄 **ETL pipeline** (Extract → Transform → Load) to MySQL
- 📊 **FastAPI endpoints** with date-range filtering
- 📈 **Interactive graphs** via web interface
- 🚀 **One-command Docker deployment**
- 🛡️ **Secure CORS** and production-ready configuration

## 🏗️ Architecture

**Layers:**
1. **Data Source** – External stock API (raw AAPL price/volume data)
2. **ETL Layer** – Python jobs: extract JSON, transform (cleaning, validation, features), load to MySQL
3. **Database** – MySQL schema optimized for time-series queries
4. **API Layer** – FastAPI REST endpoints for date-range queries
5. **Visualization** – Swagger UI + graph rendering
6. **Containerization** – Docker for portable deployment

## ✅ What Works Well

**Production-ready features:**
- ✅ **ETL extracts** live Apple stock data as validated JSON
- ✅ **Transforms** data into relational MySQL structure
- ✅ **Loads data** into optimized time-series schema
- ✅ **FastAPI endpoints** serve date-range queries with interactive graphs
- ✅ **Docker container** runs anywhere with one command
- ✅ **Secure CORS** prevents malicious access

## ⚠️ What Doesn't Work Well

**Current limitations:**
- ❌ **Single JSON overwrite** (no historical audit trail)
  - *Fix:* Timestamped files (`apple_stock_20260217_1600.json`)
- ❌ **Manual ETL trigger** (no scheduler)
- ❌ **MySQL external** (requires user setup)

## 📋 Prerequisites

| Requirement | Details |
|-------------|---------|
| [Docker](https://docker.com) | Desktop (Win/Mac) or Engine (Linux) |
| Port | 8000 free locally |
| [Git](https://git-scm.com) | For cloning |
| **MySQL** | Local or cloud (AWS RDS, Azure SQL, etc.) |

## 🔧 MySQL Setup (External - You Provide)

Your own MySQL server required (Local/Cloud):

🗄️ **MySQL Setup (REQUIRED - External)**

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
```

### 2. Configure `.env` file

```bash
# .env (create in project root)
MYSQL_HOST=localhost           # or cloud endpoint
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_secure_password
MYSQL_DATABASE=aapl_stocks
```

**Quick start:** `cp .env.example .env` then edit passwords.

## 🚀 Quick Start (2 Minutes)

```bash
git clone https://github.com/YH-DataEngineer/Apple_Stock_Data_App.git
cd Apple_Stock_Data_App
cp .env.example .env  # Open .env then edit username and passwords
docker build -t apple-stock-api .
docker run --env-file .env -p 8000:8000 apple-stock-api
```

✅ **Open:** [http://localhost:8000/docs](http://localhost:8000/docs)

## 🛠️ Local Dev (Optional)

```bash
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

## 🚀 Future Improvements

- **Scheduler** (Cron/Airflow) for automated daily ETL
- **Timestamped JSONs** for full audit trail
- **Separate DB container** for full local stack
- **Authentication/JWT** for API security
- **React dashboard** beyond Swagger UI
- **CI/CD pipeline** with GitHub Actions

## 🔧 Troubleshooting

| Problem | Fix |
|---------|-----|
| Port 8000 busy | `docker run -p 8080:8000` → `localhost:8080` |
| MySQL connection fails | Check `.env` passwords/host |
| No response | `docker logs <container-id>` |
| Build fails | `docker image prune` |

## 📁 Project Structure

```
├── test/                     # Unit testing
├── Dockerfile         # Container magic
├── .env                      # MySQL template
├── main.py             # FastAPI endpoints
├── data_extraction.py # Pulls data from API and stores in Json
├── Transformation.py     # Stock → MySQL ETL
├── mini_api.py
├── requirements.txt    # Dependencies
└── README.md
```

## 🤝 Contributing

1. Fork repo
2. `git checkout -b feature/add-symbol`
3. Commit + PR

## 📄 License

MIT - Free for learning/work!

---

**⭐ Star if useful! Questions? Open an issue.**
```

