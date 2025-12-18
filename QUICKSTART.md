# 🚀 Quick Start Guide

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

**OR** use the setup script:
```bash
python setup.py
```

## Step 2: Run the Analysis

```bash
python main.py
```

That's it! 🎉

## What You'll Get

After running, check the `outputs/` folder for:
- ✅ Year-wise transaction growth chart
- ✅ Transaction amount growth charts
- ✅ Top states bar chart
- ✅ Interactive India map (HTML file)
- ✅ Static India map (PNG file)

## Troubleshooting

### If geopandas fails to install:
```bash
conda install -c conda-forge geopandas
```

### If map PNG export fails:
The HTML map will still work! To enable PNG:
```bash
pip install kaleido
```

### If you see import errors:
Make sure you're in the project root directory when running:
```bash
cd phonepae
python main.py
```

