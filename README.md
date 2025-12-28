# 📊 PhonePe Pulse Data Visualization Dashboard

A comprehensive end-to-end data engineering and visualization project that extracts, processes, and visualizes PhonePe Pulse transaction and user data using Python, MySQL, and Streamlit.

## 🎯 Project Overview

This project provides an interactive dashboard to explore and analyze PhonePe's digital payment transactions across India. It follows a complete ETL (Extract, Transform, Load) pipeline:

1. **Extract**: Clones and extracts data from the PhonePe Pulse GitHub repository
2. **Transform**: Cleans, normalizes, and processes JSON data using Pandas
3. **Load**: Stores processed data in MySQL database
4. **Visualize**: Creates interactive visualizations using Streamlit and Plotly

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Database Setup](#-database-setup)
- [Usage](#-usage)
- [Dashboard Insights](#-dashboard-insights)
- [Screenshots](#-screenshots)
- [Learning Outcomes](#-learning-outcomes)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

- 🔄 **Automated ETL Pipeline**: Complete data pipeline from GitHub to MySQL
- 📊 **10+ Interactive Insights**: Comprehensive visualizations and analytics
- 🗺️ **Geo-visualization**: State-wise and district-wise data visualization
- 📈 **Time-series Analysis**: Year-wise and quarter-wise growth trends
- 🎛️ **Dynamic Filtering**: Filter by year, quarter, state, and transaction type
- 💾 **MySQL Integration**: Robust database storage with proper indexing
- 🎨 **Modern UI**: Beautiful Streamlit dashboard with Plotly charts

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PhonePe Pulse Dashboard                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: EXTRACT                                            │
│  ┌──────────────────┐      ┌──────────────────┐            │
│  │  Clone GitHub    │ ───► │  Extract JSON    │            │
│  │  Repository      │      │  Data Files      │            │
│  └──────────────────┘      └──────────────────┘            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 2: TRANSFORM                                          │
│  ┌──────────────────┐      ┌──────────────────┐            │
│  │  Clean Data      │ ───► │  Normalize       │            │
│  │  (Pandas)        │      │  DataFrames      │            │
│  └──────────────────┘      └──────────────────┘            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 3: LOAD                                               │
│  ┌──────────────────┐      ┌──────────────────┐            │
│  │  Batch Insert    │ ───► │  MySQL Database  │            │
│  │  Data            │      │  (6 Tables)      │            │
│  └──────────────────┘      └──────────────────┘            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 4: VISUALIZE                                          │
│  ┌──────────────────┐      ┌──────────────────┐            │
│  │  Streamlit       │ ───► │  Interactive     │            │
│  │  Dashboard       │      │  Plotly Charts   │            │
│  └──────────────────┘      └──────────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow Diagram

```
GitHub Repository (PhonePe Pulse)
         │
         │ Clone via GitPython
         ▼
    data/raw/pulse/
         │
         │ Extract JSON files
         ▼
    scripts/extract_data.py
         │
         │ Transform with Pandas
         ▼
    scripts/transform_data.py
         │
         │ Load to MySQL
         ▼
    MySQL Database
         │
         │ Query data
         ▼
    dashboard/app.py
         │
         │ Render visualizations
         ▼
    Streamlit Dashboard
```

## 🛠️ Tech Stack

### Backend & Data Processing
- **Python 3.10+**: Core programming language
- **Pandas**: Data manipulation and transformation
- **MySQL**: Relational database for data storage
- **mysql-connector-python**: MySQL database connector
- **GitPython**: GitHub repository cloning
- **python-dotenv**: Environment variable management

### Visualization & Frontend
- **Streamlit**: Web application framework
- **Plotly**: Interactive data visualization
- **JSON**: Data serialization

### Development Tools
- **PEP8**: Code style guidelines
- **Logging**: Application logging
- **Error Handling**: Comprehensive error management

## 📁 Project Structure

```
phonepe-pulse-project/
│
├── data/
│   ├── raw/                  # Cloned GitHub repository
│   │   └── pulse/
│   └── processed/            # Processed CSV files (optional)
│
├── database/
│   ├── schema.sql            # MySQL database schema
│   ├── db_connection.py      # Database connection utilities
│   └── insert_data.py        # Data insertion scripts
│
├── scripts/
│   ├── clone_repo.py         # Clone PhonePe Pulse repository
│   ├── extract_data.py       # Extract JSON data
│   └── transform_data.py     # Transform and clean data
│
├── dashboard/
│   └── app.py                # Streamlit dashboard application
│
├── utils/
│   └── helpers.py            # Utility functions
│
├── .env                      # Environment variables (create from env_example.txt)
├── .gitignore                # Git ignore rules
├── requirements.txt          # Python dependencies
├── main.py                   # Main ETL pipeline orchestrator
└── README.md                 # Project documentation
```

## 📦 Installation

### Prerequisites

- Python 3.10 or higher
- MySQL Server 8.0 or higher
- Git (for repository cloning)
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd phonepe-pulse-project
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

1. Copy `env_example.txt` to `.env`:
   ```bash
   copy env_example.txt .env  # Windows
   cp env_example.txt .env    # Linux/Mac
   ```

2. Edit `.env` file with your MySQL credentials:
   ```env
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_password_here
   DB_NAME=phonepe_pulse
   DB_PORT=3306
   ```

## 🗄️ Database Setup

### Option 1: Automatic Setup (Recommended)

The ETL pipeline will automatically create the database and tables when you run `main.py`.

### Option 2: Manual Setup

1. **Create MySQL Database**:
   ```sql
   CREATE DATABASE phonepe_pulse;
   ```

2. **Run Schema Script**:
   ```bash
   mysql -u root -p phonepe_pulse < database/schema.sql
   ```

   Or use MySQL Workbench to execute `database/schema.sql`

### Database Schema

The database contains 6 main tables:

1. **aggregated_transactions**: State-level aggregated transaction data
2. **aggregated_users**: State-level aggregated user data
3. **map_transactions**: District-level transaction data
4. **map_users**: District-level user data
5. **top_transactions**: Top performing states/districts/pincodes
6. **top_users**: Top states/districts/pincodes by registered users

Each table includes:
- Primary keys and unique constraints
- Indexed columns for performance
- Timestamp fields for data tracking

## 🚀 Usage

### Step 1: Run ETL Pipeline

Execute the main orchestrator script to clone, extract, transform, and load data:

```bash
python main.py
```

This will:
1. Create database and tables (if not exists)
2. Clone PhonePe Pulse repository
3. Extract all JSON data files
4. Transform and clean the data
5. Load data into MySQL database

**Expected Output**:
```
============================================================
Starting PhonePe Pulse ETL Pipeline
============================================================

[Step 1/4] Setting up database...
Database 'phonepe_pulse' created or already exists
Database schema created successfully!

[Step 2/4] Cloning PhonePe Pulse repository...
Repository cloned successfully to data/raw/pulse

[Step 3/4] Extracting data from repository...
Extracted 5000+ records

[Step 4/4] Transforming data...
Transformed 5000+ records

[Step 5/5] Loading data into MySQL database...
Inserted/Updated all records

============================================================
ETL Pipeline Completed Successfully!
============================================================
```

### Step 2: Launch Dashboard

Start the Streamlit dashboard:

```bash
streamlit run dashboard/app.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

### Step 3: Explore the Dashboard

Use the sidebar filters to:
- Select Year and Quarter
- Choose specific State
- Filter by Transaction Type
- Select Metric Type

## 📊 Dashboard Insights

The dashboard provides **10+ comprehensive insights**:

### 1. **Geo Visualization: Transaction Amount by State**
   - Interactive bar chart showing transaction amounts across all Indian states
   - Color-coded visualization for easy comparison

### 2. **Transaction Count by State**
   - Pie chart of top 10 states by transaction count
   - Visual representation of transaction distribution

### 3. **Registered Users by State**
   - Bar chart displaying registered users across states
   - Helps identify user adoption patterns

### 4. **App Opens by State**
   - Scatter plot comparing app opens vs registered users
   - Shows user engagement levels

### 5. **Top 10 States by Transaction Amount**
   - Histogram of highest performing states
   - Includes detailed data table

### 6. **Top 10 Districts**
   - District-level analysis grouped by state
   - Identifies high-performing regions

### 7. **Year-wise Growth Trend**
   - Time series visualization showing growth over years
   - Dual-axis chart for amount and count

### 8. **Quarter-wise Comparison**
   - Quarterly breakdown for selected year
   - Bar and line charts for comprehensive analysis

### 9. **Transaction Type Distribution**
   - Pie chart and bar chart showing transaction type breakdown
   - Analyzes payment category distribution

### 10. **User Growth Trend**
   - Historical trend of registered users and app opens
   - Period-wise analysis with dual metrics

### Additional Features

- **Key Metrics Cards**: Summary statistics at the top
- **State Comparison Table**: Complete state-wise data comparison
- **Interactive Filters**: Real-time filtering and visualization updates
- **Responsive Design**: Works on desktop and tablet devices

## 📸 Screenshots

### Dashboard Overview
*[Add your dashboard screenshots here]*

### Key Metrics Section
*[Add screenshot of metrics cards]*

### Geo Visualization
*[Add screenshot of state-wise visualization]*

### Growth Trends
*[Add screenshot of year-wise and quarter-wise charts]*

### Filtered Views
*[Add screenshot showing filtered data]*

## 🎓 Learning Outcomes

This project demonstrates:

### Data Engineering Skills
- ✅ ETL pipeline design and implementation
- ✅ Data extraction from APIs/repositories
- ✅ Data transformation and normalization
- ✅ Database design and optimization
- ✅ Batch processing techniques

### Data Analysis Skills
- ✅ Exploratory Data Analysis (EDA)
- ✅ Time-series analysis
- ✅ Geographic data visualization
- ✅ Statistical aggregation and grouping
- ✅ Data quality and cleaning

### Technical Skills
- ✅ Python programming (Pandas, MySQL, Streamlit)
- ✅ SQL database operations
- ✅ RESTful API integration (GitHub)
- ✅ Version control (Git)
- ✅ Environment management

### Visualization Skills
- ✅ Interactive dashboard creation
- ✅ Multiple chart types (bar, pie, line, scatter)
- ✅ Real-time filtering and updates
- ✅ User experience (UX) design
- ✅ Data storytelling

### Best Practices
- ✅ Code modularity and reusability
- ✅ Error handling and logging
- ✅ Security (environment variables)
- ✅ Documentation and README
- ✅ PEP8 code standards

## 🔧 Troubleshooting

### Common Issues

**1. Database Connection Error**
```
Error: Access denied for user 'root'@'localhost'
```
**Solution**: Check your MySQL credentials in `.env` file and ensure MySQL server is running.

**2. Module Not Found Error**
```
ModuleNotFoundError: No module named 'streamlit'
```
**Solution**: Install dependencies: `pip install -r requirements.txt`

**3. Repository Cloning Failed**
```
Error: Repository already exists
```
**Solution**: The script handles this automatically, or delete `data/raw/pulse` folder and rerun.

**4. No Data in Dashboard**
```
⚠️ No data found in database
```
**Solution**: Run `python main.py` first to populate the database.

**5. Port Already in Use**
```
Error: Port 8501 is already in use
```
**Solution**: Use different port: `streamlit run dashboard/app.py --server.port 8502`

## 📝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **PhonePe**: For providing open data through [PhonePe Pulse GitHub Repository](https://github.com/PhonePe/pulse)
- **Streamlit**: For the amazing dashboard framework
- **Plotly**: For interactive visualization capabilities
- **Open Source Community**: For the excellent Python libraries

## 📞 Contact & Support

For questions, issues, or suggestions:
- Open an issue on GitHub
- Check the documentation
- Review the code comments

## 🎥 Demo Video

**LinkedIn Demo Video**: *[Add your LinkedIn demo video link here]*

### Video Sections:
1. Project Overview (30 seconds)
2. ETL Pipeline Demonstration (1 minute)
3. Dashboard Walkthrough (2 minutes)
4. Key Insights and Features (1 minute)
5. Technical Highlights (30 seconds)

---

**Built with ❤️ using Python, MySQL, and Streamlit**

*Last Updated: 2024*

