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

## Viewing Stored Data

### Option 1: Using Python Script (Recommended)
Use the `view_data.py` script to view your data:

```bash
# Show summary of all tables
python view_data.py

# View specific table
python view_data.py --table aggregated_transactions

# View more records
python view_data.py --table aggregated_transactions --limit 50

# View all tables with sample data
python view_data.py --all

# Run custom SQL query
python view_data.py --query "SELECT * FROM aggregated_transactions WHERE year=2023 LIMIT 10"
```

### Option 2: Using MySQL Command Line
Connect to MySQL and query directly:

```bash
mysql -u root -p phonepe_pulse
```

Then run SQL queries:
```sql
-- Show all tables
SHOW TABLES;

-- View data from a table
SELECT * FROM aggregated_transactions LIMIT 10;

-- Count records in each table
SELECT COUNT(*) FROM aggregated_transactions;
SELECT COUNT(*) FROM aggregated_users;
SELECT COUNT(*) FROM map_transactions;
SELECT COUNT(*) FROM map_users;
SELECT COUNT(*) FROM top_transactions;
SELECT COUNT(*) FROM top_users;

-- Sample queries
SELECT state, year, SUM(transaction_amount) as total 
FROM aggregated_transactions 
GROUP BY state, year 
ORDER BY total DESC 
LIMIT 10;
```

### Option 3: Using MySQL Workbench or phpMyAdmin
- Connect using your credentials from `.env`
- Browse tables and run queries visually

### Option 4: Using Streamlit Dashboard
The dashboard provides interactive visualization:
```bash
streamlit run dashboard/app.py
```

## Next Steps

1. View your data using `python view_data.py`
2. Explore the dashboard filters
3. Check out all 10+ insights
4. Analyze year-wise and quarter-wise trends
5. Review top states and districts

Happy Analyzing! 📊

