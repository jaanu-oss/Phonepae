"""
Quick preview of what the Streamlit app will show
"""
import sys
import os

# Fix encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from scripts.data_processor import PhonePeDataProcessor
import pandas as pd

print("="*70)
print("📱 PhonePe Pulse Analysis - Data Preview")
print("="*70)

# Load data
processor = PhonePeDataProcessor(data_dir='data')
processor.load_sample_data()
processed_data = processor.process_data()

print("\n📊 YEAR-WISE SUMMARY:")
print("-"*70)
yearly = processed_data['yearly_summary']
for _, row in yearly.iterrows():
    print(f"  {int(row['Year'])}: {row['Transactions']/1e6:.2f}M transactions | ₹{row['Amount']/1e9:.2f}B")

print("\n🏆 TOP 10 STATES BY TRANSACTIONS:")
print("-"*70)
top_states = processed_data['state_summary'].head(10)
for i, (_, row) in enumerate(top_states.iterrows(), 1):
    print(f"  {i:2d}. {row['State']:20s}: {row['Transactions']/1e6:6.2f}M transactions")

print("\n📈 KEY METRICS:")
print("-"*70)
print(f"  Total States: {len(processed_data['state_summary'])}")
print(f"  Year Range: {yearly['Year'].min()} - {yearly['Year'].max()}")
print(f"  Total Transactions: {yearly['Transactions'].sum()/1e6:.2f}M")
print(f"  Total Amount: ₹{yearly['Amount'].sum()/1e12:.2f}T")

first_year = yearly.iloc[0]
last_year = yearly.iloc[-1]
growth = ((last_year['Transactions'] - first_year['Transactions']) / first_year['Transactions']) * 100
print(f"  Growth Rate (2018-2024): {growth:.1f}%")

print("\n" + "="*70)
print("✅ Streamlit App is ready!")
print("   Run: streamlit run app.py")
print("   Then open: http://localhost:8501")
print("="*70)

