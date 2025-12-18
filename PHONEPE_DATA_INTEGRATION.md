# 📊 PhonePe Pulse Real Data Integration

## ✅ Successfully Integrated!

Your project now uses **real PhonePe Pulse data** from the official GitHub repository:
**https://github.com/PhonePe/pulse**

## 🔄 How It Works

### Data Source
- **Repository**: PhonePe/pulse (Official)
- **Data Format**: JSON files organized by year/quarter
- **Update Frequency**: Quarterly (every 3 months)
- **License**: CDLA-Permissive-2.0 (Open Data License)

### Data Structure
The data is fetched from:
```
https://raw.githubusercontent.com/PhonePe/pulse/master/data/
├── map/transaction/hover/country/india/{year}/{quarter}.json
├── map/insurance/hover/country/india/{year}/{quarter}.json
└── aggregated/transaction/country/india/{year}/{quarter}.json
```

### Features

1. **Automatic Data Fetching**
   - Fetches data directly from PhonePe Pulse GitHub repository
   - Caches data locally for faster subsequent loads
   - Falls back to sample data if network issues occur

2. **Real Transaction Data**
   - State-wise transaction counts
   - Transaction amounts in INR
   - Year and quarter breakdown
   - Aggregated across quarters for yearly analysis

3. **Real Insurance Data**
   - State-wise insurance policy counts
   - Insurance values in INR
   - Same structure as transaction data

4. **Data Caching**
   - Downloaded data is cached in `data/phonepe_cache/`
   - Reduces API calls and improves performance
   - Cache files are JSON format for easy inspection

## 🚀 Usage

### In Streamlit App

The app now has a **Data Source** selector in the sidebar:
- **📊 Real PhonePe Data** - Uses actual data from GitHub (default)
- **🎲 Sample Data** - Uses simulated data for testing

### In Code

```python
from scripts.data_processor import PhonePeDataProcessor

# Load real PhonePe data
processor = PhonePeDataProcessor(data_dir='data')
processor.load_phonepe_data(use_real=True, years=[2021, 2022, 2023, 2024])

# Process the data
processed_data = processor.process_data()

# Access the data
state_summary = processed_data['state_summary']
insurance_summary = processed_data.get('insurance_summary')
```

## 📁 Data Files

### Cached Data Location
```
data/
└── phonepe_cache/
    ├── map_trans_2024_4.json
    ├── map_ins_2024_4.json
    └── ...
```

### Data Structure

**Transaction Data:**
- `Year`: Transaction year
- `State`: State name
- `Transactions`: Total transaction count
- `Amount`: Total transaction amount (INR)

**Insurance Data:**
- `Year`: Insurance year
- `State`: State name
- `Policies`: Total insurance policy count
- `Value`: Total insurance value (INR)

## 🔧 Configuration

### Available Years
- 2018, 2019, 2020, 2021, 2022, 2023, 2024

### Available Quarters
- Q1 (Jan-Mar)
- Q2 (Apr-Jun)
- Q3 (Jul-Sep)
- Q4 (Oct-Dec)

### Default Settings
- **Years**: 2021-2024 (most recent with complete data)
- **Quarters**: All 4 quarters
- **Aggregation**: Summed across quarters for yearly totals

## 📊 Data Quality

### What's Included
✅ Real transaction volumes from PhonePe
✅ Real state-wise distribution
✅ Real insurance data (when available)
✅ Historical data from 2018-2024
✅ Quarterly granularity

### Data Limitations
- Some older years may have incomplete data
- District-level data requires additional API calls
- Network dependency for initial fetch

## 🛠️ Troubleshooting

### Issue: Data not loading
**Solution**: Check internet connection. The app will fall back to sample data automatically.

### Issue: Slow loading
**Solution**: Data is cached after first load. Subsequent loads are much faster.

### Issue: Missing states
**Solution**: Some states may not have data for all quarters. The processor handles this gracefully.

### Issue: Cache issues
**Solution**: Delete `data/phonepe_cache/` folder to force fresh download.

## 📝 Notes

- Data is fetched in real-time from GitHub
- No API key or authentication required
- Data is publicly available under CDLA-Permissive-2.0 license
- Respects PhonePe's data usage policies
- Caching improves performance significantly

## 🔗 References

- **PhonePe Pulse Repository**: https://github.com/PhonePe/pulse
- **PhonePe Pulse Website**: https://www.phonepe.com/pulse/
- **Data License**: CDLA-Permissive-2.0

---

**Last Updated**: Data integration completed successfully! 🎉

