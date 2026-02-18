AAPL Stock API
AAPL Stock API is a Dockerized FastAPI app that fetches real-time Apple stock data, processes it through an ETL pipeline into MySQL, and serves interactive graph endpoints. Users query date ranges via a clean Swagger UI to visualize stock trends with zero local setup required.

[

✨ Features
Fetches real-time AAPL stock data

ETL pipeline (Extract → Transform → Load) into MySQL

FastAPI endpoints with date-range filtering

Interactive graphs via web interface

One-command Docker deployment

📋 Prerequisites
Docker installed (Desktop for Windows/Mac, Engine for Linux)

Port 8000 free on your machine

Git (for cloning)

No Python, MySQL, or dependencies needed - everything runs in Docker!

🔧 MySQL Configuration
The app uses environment variables to connect to MySQL. Create a .env file in the project root:

bash
# .env file (create this file)
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_secure_password
MYSQL_DATABASE=aapl_stocks
MYSQL_ROOT_PASSWORD=your_secure_password
Copy-paste these defaults and change passwords:

bash
cp .env.example .env
# Edit .env with your values
Run with custom MySQL settings:

bash
docker run --env-file .env -p 8000:8000 aapl-stock-api
Default values (if no .env file):

text
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=admin123
MYSQL_DATABASE=aapl_stocks
💡 Pro tip: Always use .env for security - never hardcode passwords!

🚀 Quick Start (2 minutes)
bash
# 1. Clone the project
git clone https://github.com/yourusername/aapl-stock-api.git
cd aapl-stock-api

# 2. (Optional) Set up MySQL - copy example env file
cp .env.example .env
nano .env  # Edit passwords

# 3. Build Docker image  
docker build -t aapl-stock-api .

# 4. Run the app
docker run --env-file .env -p 8000:8000 aapl-stock-api
✅ Done! Open http://localhost:8000/docs to test endpoints.

🎮 Using the API
Visit http://localhost:8000/docs (automatic Swagger UI)

Select date range (e.g., "2025-01-01 to 2025-02-01")

Get JSON response with stock data

View interactive graphs

Example endpoint:

text
GET /stocks?start_date=2025-01-01&end_date=2025-02-18
🌐 Network Access
Use localhost:8000 or 127.0.0.1:8000 - NOT 0.0.0.0:8000

Works ✅	Doesn't Work ❌	Why?
localhost:8000	0.0.0.0:8000	0.0.0.0 is for Docker server binding, not browser access
127.0.0.1:8000		Both point to your container
Your Docker is perfect! Port mapping forwards localhost:8000 → container correctly.

🐳 Docker Architecture
text
GitHub Repo + .env
   ↓ clone
Docker Build ──► Image (FastAPI + MySQL + Stock ETL)
   ↓ docker run + --env-file  
Container ──► Port 8000 ──► localhost:8000
🔧 Troubleshooting
Issue	Solution
Port 8000 already in use	Use docker run -p 8080:8000 → visit localhost:8080
0.0.0.0:8000 doesn't work	Use localhost:8000 or 127.0.0.1:8000
MySQL connection refused	Check .env passwords match; restart container
Container shows but no response	Check logs: docker logs <container-id>
Build fails	Delete old images: docker image prune
Pro tip: See running containers: docker ps

🛠️ Development (Optional)
If Docker has issues, run locally:

bash
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
📁 Project Structure
text
├── test/                    # Demo tests (pytest) ✅
├── Dockerfile              # Builds everything
├── .env.example           # MySQL config template
├── main.py                # FastAPI app + endpoints  
├── etl_pipeline.py        # Stock data → MySQL
├── requirements.txt       # Python deps
└── README.md              # You're reading it!
🤝 Contributing
Fork the repo

Create feature branch (git checkout -b feature/stock-data)

Commit changes (git commit -m 'Add new stock endpoint')

Push (git push origin feature/stock-data)

Open Pull Request

📄 License
MIT License - use freely for learning/work projects.

👨‍💼 Presenter Notes
Demo flow: Clone → Edit .env → Build → Run → localhost:8000/docs → Query dates → Graph appears

Key selling points: Zero setup, secure env vars, production-ready Docker, full test suite

Time: 3-minute live demo

