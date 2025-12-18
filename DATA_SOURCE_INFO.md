# 📊 PhonePe Pulse Data Source Information

## Current Data Source

**⚠️ Important:** The current implementation uses **simulated/sample data**, not real PhonePe Pulse data.

### How Current Data is Generated

The data is generated in `scripts/data_processor.py` using the `load_sample_data()` function:

1. **Years**: 2018-2024 (7 years)
2. **States**: 29 Indian states and union territories
3. **Generation Method**: 
   - Uses NumPy random number generation with a fixed seed (42) for reproducibility
   - Simulates 30% growth per year
   - Random transaction amounts between ₹500-₹5000
   - Creates realistic-looking data structure matching PhonePe Pulse format

### Why Sample Data?

- PhonePe Pulse API requires authentication and may have usage restrictions
- Sample data allows the project to run immediately without API setup
- Demonstrates the visualization capabilities
- Useful for development and testing

---

## How to Get Real PhonePe Pulse Data

### Option 1: PhonePe Pulse Website
1. Visit: **https://www.phonepe.com/pulse/**
2. Navigate to "Explore Data" section
3. Download data for specific:
   - Years (2018-2024)
   - Quarters (Q1-Q4)
   - States
   - Districts
   - Transaction types

### Option 2: PhonePe Pulse Data APIs
PhonePe provides data APIs (may require registration):
- Check: **https://www.phonepe.com/pulse/data-apis/**
- API endpoints for:
  - Transaction data
  - Insurance data
  - State-wise data
  - District-wise data

### Option 3: Manual Data Collection
1. Visit PhonePe Pulse website
2. Use browser developer tools to inspect API calls
3. Extract data from API responses
4. Save as CSV or JSON files

### Option 4: Public Datasets
Some researchers/developers share PhonePe Pulse data:
- GitHub repositories
- Kaggle datasets
- Research papers with data links

---

## How to Use Real Data

### Step 1: Prepare Your Data File

Create a CSV or JSON file with this structure:

**CSV Format:**
```csv
Year,State,District,Transactions,Amount
2024,Maharashtra,Mumbai,5000000,25000000000
2024,Maharashtra,Pune,3000000,15000000000
...
```

**JSON Format:**
```json
[
  {
    "Year": 2024,
    "State": "Maharashtra",
    "District": "Mumbai",
    "Transactions": 5000000,
    "Amount": 25000000000
  },
  ...
]
```

### Step 2: Update the Code

In `app.py` or `main.py`, modify the data loading:

```python
# Instead of:
processor.load_sample_data()

# Use:
processor.load_from_file('your_phonepe_data.csv')
# or
processor.load_from_file('your_phonepe_data.json')
```

### Step 3: Place Data File

Put your data file in the `data/` folder:
```
phonepae/
└── data/
    └── your_phonepe_data.csv  (or .json)
```

---

## Data Structure Requirements

Your data file should have these columns/fields:

### Required Fields:
- **Year**: Transaction year (2018-2024)
- **State**: State name (e.g., "Maharashtra", "Karnataka")
- **Transactions**: Number of transactions (integer)
- **Amount**: Total transaction amount in INR (integer/float)

### Optional Fields:
- **District**: District name (for district-level analysis)
- **Quarter**: Q1, Q2, Q3, Q4 (for quarterly analysis)
- **Transaction_Type**: UPI, Cards, Wallets, etc.

---

## Example: Fetching from PhonePe Pulse API

If PhonePe provides an API, you could modify `data_processor.py`:

```python
def fetch_from_phonepe_api(self, year, quarter):
    """
    Fetch real data from PhonePe Pulse API
    Requires API key/authentication
    """
    import requests
    
    api_url = "https://api.phonepe.com/pulse/data"
    headers = {
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json"
    }
    
    params = {
        "year": year,
        "quarter": quarter
    }
    
    response = requests.get(api_url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        # Process and return data
        return data
    else:
        raise Exception(f"API Error: {response.status_code}")
```

---

## Current Sample Data Details

**What's Generated:**
- ✅ 29 states/UTs
- ✅ 7 years (2018-2024)
- ✅ Realistic transaction volumes
- ✅ Growth patterns over time
- ✅ District data (for major states)

**What's NOT Real:**
- ❌ Actual PhonePe transaction numbers
- ❌ Real state-wise distribution
- ❌ Actual growth rates
- ❌ Real district names (except for major states)

---

## Recommendations

1. **For Demo/Portfolio**: Current sample data is perfect
2. **For Real Analysis**: 
   - Download data from PhonePe Pulse website
   - Or integrate with PhonePe Pulse API (if available)
   - Or use publicly available PhonePe datasets

3. **For Production**: 
   - Set up automated data fetching
   - Implement data validation
   - Add error handling for API calls
   - Cache data to reduce API calls

---

**Note**: Always respect PhonePe's terms of service and data usage policies when accessing their data.

