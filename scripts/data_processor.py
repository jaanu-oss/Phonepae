"""
Data Processor for PhonePe Pulse Data
Handles data loading, cleaning, and aggregation
Supports both sample data and real PhonePe Pulse data from GitHub
"""

import pandas as pd
import numpy as np
import os
import json
import requests
from typing import Dict, List, Optional


class PhonePeDataProcessor:
    def __init__(self, data_dir='data', use_real_data=False):
        self.data_dir = data_dir
        self.raw_data = None
        self.processed_data = None
        self.use_real_data = use_real_data
        self.base_url = "https://raw.githubusercontent.com/PhonePe/pulse/master/data"
        self.cache_dir = os.path.join(data_dir, 'phonepe_cache')
        os.makedirs(self.cache_dir, exist_ok=True)
        
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
        
        # Add insurance summary if available
        if hasattr(self, 'insurance_data') and self.insurance_data is not None:
            self.processed_data['insurance_summary'] = self.insurance_data.groupby('State').agg({
                'Policies': 'sum',
                'Value': 'sum'
            }).reset_index()
            self.processed_data['insurance_summary'].columns = ['State', 'Insurance_Policies', 'Insurance_Value']
        
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
    
    def fetch_phonepe_json(self, url: str, cache_file: str = None) -> Optional[Dict]:
        """Fetch JSON data from PhonePe Pulse GitHub repository with caching"""
        if cache_file:
            cache_path = os.path.join(self.cache_dir, cache_file)
            if os.path.exists(cache_path):
                try:
                    with open(cache_path, 'r', encoding='utf-8') as f:
                        return json.load(f)
                except:
                    pass
        
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if cache_file and data:
                    with open(cache_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                return data
        except Exception as e:
            print(f"Warning: Could not fetch {url}: {str(e)}")
        return None
    
    def load_real_phonepe_data(self, years: List[int] = None, quarters: List[int] = None):
        """Load real PhonePe Pulse data from GitHub repository"""
        if years is None:
            years = [2021, 2022, 2023, 2024]  # Most recent years with data
        if quarters is None:
            quarters = [1, 2, 3, 4]
        
        print("Fetching real PhonePe Pulse data from GitHub...")
        print(f"   Repository: https://github.com/PhonePe/pulse")
        
        all_transaction_data = []
        all_insurance_data = []
        
        for year in years:
            for quarter in quarters:
                # Fetch transaction map data (state-level)
                trans_url = f"{self.base_url}/map/transaction/hover/country/india/{year}/{quarter}.json"
                cache_file = f"map_trans_{year}_{quarter}.json"
                trans_data = self.fetch_phonepe_json(trans_url, cache_file)
                
                if trans_data and 'data' in trans_data and 'hoverDataList' in trans_data['data']:
                    for item in trans_data['data']['hoverDataList']:
                        state_name = item.get('name', '').title()
                        if 'metric' in item and isinstance(item['metric'], list):
                            for metric in item['metric']:
                                if metric.get('type') == 'TOTAL':
                                    all_transaction_data.append({
                                        'Year': year,
                                        'Quarter': quarter,
                                        'State': state_name,
                                        'Transactions': metric.get('count', 0),
                                        'Amount': metric.get('amount', 0)
                                    })
                
                # Fetch insurance map data
                ins_url = f"{self.base_url}/map/insurance/hover/country/india/{year}/{quarter}.json"
                cache_file_ins = f"map_ins_{year}_{quarter}.json"
                ins_data = self.fetch_phonepe_json(ins_url, cache_file_ins)
                
                if ins_data and 'data' in ins_data and 'hoverDataList' in ins_data['data']:
                    for item in ins_data['data']['hoverDataList']:
                        state_name = item.get('name', '').title()
                        if 'metric' in item and isinstance(item['metric'], list):
                            for metric in item['metric']:
                                if metric.get('type') == 'TOTAL':
                                    all_insurance_data.append({
                                        'Year': year,
                                        'Quarter': quarter,
                                        'State': state_name,
                                        'Policies': metric.get('count', 0),
                                        'Value': metric.get('amount', 0)
                                    })
                
                print(f"   Loaded {year} Q{quarter}")
        
        if all_transaction_data:
            self.raw_data = pd.DataFrame(all_transaction_data)
            # Aggregate by year (sum across quarters)
            self.raw_data = self.raw_data.groupby(['Year', 'State']).agg({
                'Transactions': 'sum',
                'Amount': 'sum'
            }).reset_index()
            print(f"Loaded {len(self.raw_data)} state-year transaction records")
        
        # Store insurance data separately
        if all_insurance_data:
            self.insurance_data = pd.DataFrame(all_insurance_data)
            self.insurance_data = self.insurance_data.groupby(['Year', 'State']).agg({
                'Policies': 'sum',
                'Value': 'sum'
            }).reset_index()
            print(f"Loaded {len(self.insurance_data)} state-year insurance records")
        else:
            self.insurance_data = None
        
        if all_transaction_data:
            return self.raw_data
        else:
            print("Warning: Could not fetch real data, using sample data instead")
            return self.load_sample_data()
    
    def load_phonepe_data(self, use_real: bool = True, years: List[int] = None):
        """Main method to load PhonePe data (real or sample)"""
        if use_real:
            try:
                return self.load_real_phonepe_data(years=years)
            except Exception as e:
                print(f"Warning: Error loading real data: {str(e)}")
                print("   Falling back to sample data...")
                return self.load_sample_data()
        else:
            return self.load_sample_data()

