# 📱 PhonePe Pulse: Digital Payment Growth Analysis in India

## 🎯 Project Overview

This project analyzes the growth of digital payments in India using PhonePe Pulse data and highlights regional adoption trends. It provides comprehensive visualizations showing transaction growth patterns across different states and years.

## 📌 Features

### Visualizations

1. **Year-wise Transaction Growth** - Line chart showing total transactions vs year
2. **Transaction Amount Growth** - Line and bar charts showing monetary growth
3. **Top States by Transactions** - Horizontal bar chart of top performing states
4. **India Map (State-wise Transactions)** - Interactive choropleth map showing regional distribution

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd phonepae
   ```

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   **Note for Windows users:** If you encounter issues with `geopandas`, you may need to install it separately:
   ```bash
   pip install geopandas
   ```
   
   Or use conda:
   ```bash
   conda install geopandas
   ```

### Running the Project

Simply run the main script:

```bash
python main.py
```

This will:
1. Generate sample PhonePe Pulse data
2. Process and aggregate the data
3. Create all 4 visualizations
4. Save outputs to the `outputs/` folder

## 📁 Project Structure

```
phonepae/
├── data/                  # Data storage directory
│   └── processed_data.json
├── scripts/               # Python scripts
│   ├── data_processor.py  # Data loading and processing
│   └── visualizations.py # Visualization generation
├── outputs/              # Generated visualizations
│   ├── 1_yearly_transaction_growth.png
│   ├── 2_transaction_amount_growth.png
│   ├── 3_top_states_by_transactions.png
│   ├── 4_india_map_choropleth.html (Interactive)
│   └── 4_india_map_choropleth.png (Static)
├── main.py               # Main entry point
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 📊 Output Files

After running the script, you'll find the following files in the `outputs/` folder:

1. **1_yearly_transaction_growth.png** - Line chart showing year-over-year transaction growth
2. **2_transaction_amount_growth.png** - Combined line and bar charts for amount growth
3. **3_top_states_by_transactions.png** - Bar chart of top 10 states
4. **4_india_map_choropleth.html** - Interactive map (open in browser)
5. **4_india_map_choropleth.png** - Static map image

## 🔧 Customization

### Using Your Own Data

To use your own PhonePe Pulse data:

1. Place your data file (CSV or JSON) in the `data/` folder
2. Modify `main.py` to load your data:
   ```python
   processor.load_from_file('your_data.csv')
   ```

### Adjusting Visualizations

Edit `scripts/visualizations.py` to customize:
- Colors and styles
- Chart sizes
- Number of top states displayed
- Map styling

## 📦 Dependencies

- **pandas** - Data manipulation and analysis
- **numpy** - Numerical computing
- **matplotlib** - Static visualizations
- **seaborn** - Enhanced statistical plots
- **plotly** - Interactive visualizations and maps
- **geopandas** - Geospatial data handling
- **folium** - Alternative mapping library
- **requests** - API calls (if fetching live data)

## 🧠 Project Explanation

**"This project analyzes the growth of digital payments in India using PhonePe Pulse data and highlights regional adoption trends."**

The analysis demonstrates:
- **Temporal Trends**: How digital payments have evolved over years
- **Geographic Patterns**: Which states lead in digital payment adoption
- **Growth Metrics**: Both transaction volume and monetary value growth
- **Visual Storytelling**: Multiple visualization types for comprehensive insights

## 🐛 Troubleshooting

### Issue: geopandas installation fails
**Solution:** Use conda instead of pip:
```bash
conda install -c conda-forge geopandas
```

### Issue: Map visualization not working
**Solution:** Ensure plotly and kaleido are installed:
```bash
pip install plotly kaleido
```

### Issue: Font or display issues
**Solution:** Install required system fonts or adjust matplotlib backend:
```python
import matplotlib
matplotlib.use('Agg')  # Add this before importing pyplot
```

## 📝 Notes

- The current implementation uses **sample data** that simulates PhonePe Pulse data structure
- For production use, integrate with the actual PhonePe Pulse API or load real data files
- The choropleth map uses a public GeoJSON file for India's state boundaries

## 🤝 Contributing

Feel free to enhance this project by:
- Adding more visualization types
- Integrating with real PhonePe Pulse API
- Adding data export functionality
- Implementing interactive dashboards

## 📄 License

This project is for educational and analysis purposes.

---

**Built with ❤️ for analyzing India's digital payment revolution**

