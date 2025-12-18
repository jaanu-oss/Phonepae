"""
Main Script for PhonePe Pulse Data Analysis
Digital Payment Growth Analysis in India
"""

import sys
import os

# Fix encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from scripts.data_processor import PhonePeDataProcessor
from scripts.visualizations import PhonePeVisualizations


def main():
    """
    Main function to run the complete analysis pipeline
    """
    print("\n" + "="*70)
    print("🚀 PhonePe Pulse: Digital Payment Growth Analysis in India")
    print("="*70 + "\n")
    
    # Step 1: Initialize data processor
    print("📥 Step 1: Loading and processing data...")
    processor = PhonePeDataProcessor(data_dir='data')
    
    # Load sample data (in production, this would load from API/files)
    processor.load_sample_data()
    
    # Process the data
    processed_data = processor.process_data()
    
    # Save processed data
    processor.save_processed_data('processed_data.json')
    print("✅ Data processing completed!\n")
    
    # Step 2: Generate visualizations
    print("📊 Step 2: Generating visualizations...")
    visualizer = PhonePeVisualizations(processed_data, output_dir='outputs')
    
    # Generate all visualizations
    visualizer.generate_all_visualizations()
    
    # Step 3: Display summary statistics
    print("\n" + "="*70)
    print("📈 Summary Statistics")
    print("="*70)
    
    yearly_summary = processed_data['yearly_summary']
    state_summary = processed_data['state_summary']
    
    print(f"\n📅 Year Range: {yearly_summary['Year'].min()} - {yearly_summary['Year'].max()}")
    print(f"📊 Total States Analyzed: {len(state_summary)}")
    print(f"💰 Total Transactions (All Years): {yearly_summary['Transactions'].sum():,.0f}")
    print(f"💵 Total Amount (All Years): ₹{yearly_summary['Amount'].sum()/1e12:.2f} Trillion")
    
    print(f"\n🏆 Top 5 States by Transactions:")
    for i, row in state_summary.head(5).iterrows():
        print(f"   {i+1}. {row['State']}: {row['Transactions']/1e6:.2f}M transactions")
    
    print(f"\n📈 Growth Rate:")
    first_year = yearly_summary.iloc[0]
    last_year = yearly_summary.iloc[-1]
    growth_rate = ((last_year['Transactions'] - first_year['Transactions']) / 
                   first_year['Transactions']) * 100
    print(f"   {first_year['Year']} to {last_year['Year']}: {growth_rate:.1f}% growth")
    
    print("\n" + "="*70)
    print("✅ Analysis Complete! Check the 'outputs' folder for all visualizations.")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

