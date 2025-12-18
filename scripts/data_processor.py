"""
Data Processor for PhonePe Pulse Data
Handles data loading, cleaning, and aggregation
"""

import pandas as pd
import numpy as np
import os
import json


class PhonePeDataProcessor:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.raw_data = None
        self.processed_data = None
        
    def load_sample_data(self):
        """
        Creates sample PhonePe Pulse data structure
        In production, this would fetch from PhonePe Pulse API or load from files
        """
        # Sample data structure based on PhonePe Pulse format
        years = [2018, 2019, 2020, 2021, 2022, 2023, 2024]
        states = [
            'Maharashtra', 'Karnataka', 'Tamil Nadu', 'Uttar Pradesh', 
            'Gujarat', 'Rajasthan', 'West Bengal', 'Madhya Pradesh',
            'Delhi', 'Punjab', 'Haryana', 'Kerala', 'Odisha', 'Bihar',
            'Andhra Pradesh', 'Telangana', 'Assam', 'Jharkhand', 'Chhattisgarh',
            'Himachal Pradesh', 'Uttarakhand', 'Goa', 'Tripura', 'Manipur',
            'Meghalaya', 'Nagaland', 'Mizoram', 'Sikkim', 'Arunachal Pradesh'
        ]
        
        # Generate realistic sample data
        np.random.seed(42)
        data = []
        
        for year in years:
            for state in states:
                # Simulate growth over years
                base_transactions = np.random.randint(100000, 5000000)
                growth_factor = 1 + (year - 2018) * 0.3  # 30% growth per year
                transactions = int(base_transactions * growth_factor)
                
                # Average transaction amount (in INR)
                avg_amount = np.random.randint(500, 5000)
                total_amount = transactions * avg_amount
                
                data.append({
                    'Year': year,
                    'State': state,
                    'Transactions': transactions,
                    'Amount': total_amount,
                    'Avg_Amount': avg_amount
                })
        
        self.raw_data = pd.DataFrame(data)
        return self.raw_data
    
    def process_data(self):
        """Process and aggregate the raw data"""
        if self.raw_data is None:
            self.load_sample_data()
        
        self.processed_data = {
            'yearly_summary': self.raw_data.groupby('Year').agg({
                'Transactions': 'sum',
                'Amount': 'sum'
            }).reset_index(),
            
            'state_summary': self.raw_data.groupby('State').agg({
                'Transactions': 'sum',
                'Amount': 'sum'
            }).reset_index().sort_values('Transactions', ascending=False),
            
            'state_year_data': self.raw_data.groupby(['State', 'Year']).agg({
                'Transactions': 'sum',
                'Amount': 'sum'
            }).reset_index(),
            
            'full_data': self.raw_data
        }
        
        return self.processed_data
    
    def save_processed_data(self, filename='processed_data.json'):
        """Save processed data to JSON file"""
        if self.processed_data is None:
            self.process_data()
        
        output_path = os.path.join(self.data_dir, filename)
        
        # Convert to JSON-serializable format
        data_dict = {
            'yearly_summary': self.processed_data['yearly_summary'].to_dict('records'),
            'state_summary': self.processed_data['state_summary'].to_dict('records'),
            'state_year_data': self.processed_data['state_year_data'].to_dict('records')
        }
        
        with open(output_path, 'w') as f:
            json.dump(data_dict, f, indent=2)
        
        print(f"Processed data saved to {output_path}")
    
    def load_from_file(self, filename):
        """Load data from CSV or JSON file"""
        filepath = os.path.join(self.data_dir, filename)
        
        if filename.endswith('.csv'):
            self.raw_data = pd.read_csv(filepath)
        elif filename.endswith('.json'):
            with open(filepath, 'r') as f:
                data = json.load(f)
                self.raw_data = pd.DataFrame(data)
        else:
            raise ValueError("Unsupported file format. Use CSV or JSON.")
        
        return self.raw_data

