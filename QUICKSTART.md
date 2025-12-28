# 🚀 Quick Start Guide

## Prerequisites Checklist

- [ ] Python 3.10+ installed
- [ ] MySQL Server 8.0+ installed and running
- [ ] Git installed
- [ ] Virtual environment (recommended)

## Quick Setup (5 Minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Database
Copy `env_example.txt` to `.env` and update MySQL credentials:
```bash
copy env_example.txt .env  # Windows
cp env_example.txt .env    # Linux/Mac
```

Edit `.env`:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=phonepe_pulse
DB_PORT=3306
```

### 3. Run ETL Pipeline
```bash
python main.py
```

This will:
- Clone PhonePe Pulse repository
- Extract and transform data
- Create database and tables
- Load data into MySQL

**Expected time: 5-10 minutes depending on internet speed**

### 4. Launch Dashboard
```bash
streamlit run dashboard/app.py
```

Dashboard opens at: `http://localhost:8501`

## Troubleshooting

**Issue**: Database connection failed
- Check MySQL is running: `mysql --version`
- Verify credentials in `.env`
- Ensure MySQL user has create database privileges

**Issue**: No data in dashboard
- Verify ETL completed successfully
- Check database has data: `SELECT COUNT(*) FROM aggregated_transactions;`
- Check logs in `etl_pipeline.log`

**Issue**: Port 8501 already in use
```bash
streamlit run dashboard/app.py --server.port 8502
```

## Next Steps

1. Explore the dashboard filters
2. Check out all 10+ insights
3. Analyze year-wise and quarter-wise trends
4. Review top states and districts

Happy Analyzing! 📊

