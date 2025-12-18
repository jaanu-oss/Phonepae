# 🚀 Streamlit App Guide

## Running the Streamlit App

The Streamlit app provides an interactive dashboard with a proper choropleth map of India!

### Quick Start

1. **Install dependencies** (if not already done):
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

3. **Open your browser**:
   - The app will automatically open at `http://localhost:8501`
   - If it doesn't, copy the URL shown in the terminal

### Features

The Streamlit app has 4 pages:

1. **Dashboard** - Overview with key metrics and charts
2. **Year-wise Growth** - Detailed year-over-year analysis
3. **State Analysis** - State-wise breakdown with interactive filters
4. **Interactive Map** - **Proper choropleth map with India state boundaries!**

### The Map Page

The "Interactive Map" page shows:
- ✅ **Real choropleth map** with India's state boundaries
- ✅ Color-coded states based on transaction volume
- ✅ Interactive hover tooltips
- ✅ Zoom and pan capabilities
- ✅ Data table below the map

The map uses:
- GeoJSON data for accurate state boundaries
- Plotly's choropleth visualization
- Fallback to enhanced scatter map if GeoJSON unavailable

### Troubleshooting

**If the map shows only markers:**
- The app will try to fetch GeoJSON from a public source
- If that fails, it shows an enhanced scatter map with state labels
- Check your internet connection for GeoJSON fetch

**If Streamlit doesn't start:**
- Make sure port 8501 is not in use
- Try: `streamlit run app.py --server.port 8502`

**To stop the app:**
- Press `Ctrl+C` in the terminal

### Tips

- Use the sidebar to navigate between pages
- The map is fully interactive - zoom, pan, and hover!
- All charts are interactive Plotly visualizations
- Data is cached for faster loading

---

Enjoy exploring the PhonePe Pulse data! 📱📊

