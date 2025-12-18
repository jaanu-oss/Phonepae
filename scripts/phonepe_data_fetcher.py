"""
PhonePe Pulse Data Fetcher
Fetches real data from PhonePe Pulse GitHub repository
Repository: https://github.com/PhonePe/pulse.git
"""

import pandas as pd
import numpy as np
import os
import json
import requests
from typing import Dict, List, Optional


class PhonePePulseDataFetcher:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.base_url = "https://raw.githubusercontent.com/PhonePe/pulse/master/data"
        self.cache_dir = os.path.join(data_dir, 'phonepe_cache')
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def fetch_json(self, url: str, cache_file: str = None) -> Optional[Dict]:
        """Fetch JSON data from URL with caching"""
        if cache_file:
            cache_path = os.path.join(self.cache_dir, cache_file)
            if os.path.exists(cache_path):
                try:
                    with open(cache_path, 'r', encoding='utf-8') as f:
                        return json.load(f)
                except:
                    pass
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if cache_file:
                    with open(cache_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                return data
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
        return None
    
    def get_aggregated_transaction_data(self, year: int, quarter: int) -> Optional[Dict]:
        """Fetch aggregated transaction data for a year-quarter"""
        url = f"{self.base_url}/aggregated/transaction/country/india/{year}/{quarter}.json"
        cache_file = f"agg_trans_{year}_{quarter}.json"
        return self.fetch_json(url, cache_file)
    
    def get_map_transaction_data(self, year: int, quarter: int) -> Optional[Dict]:
        """Fetch map transaction data (state/district level)"""
        url = f"{self.base_url}/map/transaction/hover/country/india/{year}/{quarter}.json"
        cache_file = f"map_trans_{year}_{quarter}.json"
        return self.fetch_json(url, cache_file)
    
    def get_top_transaction_data(self, year: int, quarter: int) -> Optional[Dict]:
        """Fetch top transaction data"""
        url = f"{self.base_url}/top/transaction/country/india/{year}/{quarter}.json"
        cache_file = f"top_trans_{year}_{quarter}.json"
        return self.fetch_json(url, cache_file)
    
    def get_aggregated_insurance_data(self, year: int, quarter: int) -> Optional[Dict]:
        """Fetch aggregated insurance data"""
        url = f"{self.base_url}/aggregated/insurance/country/india/{year}/{quarter}.json"
        cache_file = f"agg_ins_{year}_{quarter}.json"
        return self.fetch_json(url, cache_file)
    
    def get_map_insurance_data(self, year: int, quarter: int) -> Optional[Dict]:
        """Fetch map insurance data (state/district level)"""
        url = f"{self.base_url}/map/insurance/hover/country/india/{year}/{quarter}.json"
        cache_file = f"map_ins_{year}_{quarter}.json"
        return self.fetch_json(url, cache_file)
    
    def get_state_transaction_data(self, state: str, year: int, quarter: int) -> Optional[Dict]:
        """Fetch transaction data for a specific state"""
        state_lower = state.lower().replace(' ', '-')
        url = f"{self.base_url}/map/transaction/hover/country/india/state/{state_lower}/{year}/{quarter}.json"
        cache_file = f"state_trans_{state_lower}_{year}_{quarter}.json"
        return self.fetch_json(url, cache_file)
    
    def parse_transaction_data(self, data: Dict) -> pd.DataFrame:
        """Parse PhonePe Pulse transaction data into DataFrame"""
        records = []
        
        if not data or 'data' not in data:
            return pd.DataFrame()
        
        data_section = data['data']
        
        # Handle aggregated data structure
        if 'data' in data_section and isinstance(data_section['data'], dict):
            for state_name, state_data in data_section['data'].items():
                if isinstance(state_data, dict):
                    for transaction_type, type_data in state_data.items():
                        if isinstance(type_data, dict) and 'data' in type_data:
                            for year_quarter, metrics in type_data['data'].items():
                                if isinstance(metrics, list):
                                    for metric in metrics:
                                        records.append({
                                            'State': state_name.title(),
                                            'Transaction_Type': transaction_type,
                                            'Year_Quarter': year_quarter,
                                            'Transactions': metric.get('paymentInstruments', [{}])[0].get('count', 0) if metric.get('paymentInstruments') else 0,
                                            'Amount': metric.get('paymentInstruments', [{}])[0].get('amount', 0) if metric.get('paymentInstruments') else 0
                                        })
        
        # Handle map hover data structure
        elif 'hoverDataList' in data_section:
            for item in data_section['hoverDataList']:
                state_name = item.get('name', '').title()
                if 'metric' in item and isinstance(item['metric'], list):
                    for metric in item['metric']:
                        records.append({
                            'State': state_name,
                            'Transaction_Type': metric.get('type', 'TOTAL'),
                            'Transactions': metric.get('count', 0),
                            'Amount': metric.get('amount', 0)
                        })
        
        return pd.DataFrame(records)
    
    def parse_insurance_data(self, data: Dict) -> pd.DataFrame:
        """Parse PhonePe Pulse insurance data into DataFrame"""
        records = []
        
        if not data or 'data' not in data:
            return pd.DataFrame()
        
        data_section = data['data']
        
        # Handle map hover data structure for insurance
        if 'hoverDataList' in data_section:
            for item in data_section['hoverDataList']:
                state_name = item.get('name', '').title()
                if 'metric' in item and isinstance(item['metric'], list):
                    for metric in item['metric']:
                        records.append({
                            'State': state_name,
                            'Insurance_Type': metric.get('type', 'TOTAL'),
                            'Policies': metric.get('count', 0),
                            'Value': metric.get('amount', 0)
                        })
        
        return pd.DataFrame(records)
    
    def load_all_transaction_data(self, years: List[int] = None, quarters: List[int] = None) -> pd.DataFrame:
        """Load all available transaction data"""
        if years is None:
            years = [2018, 2019, 2020, 2021, 2022, 2023, 2024]
        if quarters is None:
            quarters = [1, 2, 3, 4]
        
        all_data = []
        
        for year in years:
            for quarter in quarters:
                print(f"Fetching transaction data for {year} Q{quarter}...")
                data = self.get_map_transaction_data(year, quarter)
                if data:
                    df = self.parse_transaction_data(data)
                    if not df.empty:
                        df['Year'] = year
                        df['Quarter'] = quarter
                        all_data.append(df)
        
        if all_data:
            return pd.concat(all_data, ignore_index=True)
        return pd.DataFrame()
    
    def load_all_insurance_data(self, years: List[int] = None, quarters: List[int] = None) -> pd.DataFrame:
        """Load all available insurance data"""
        if years is None:
            years = [2018, 2019, 2020, 2021, 2022, 2023, 2024]
        if quarters is None:
            quarters = [1, 2, 3, 4]
        
        all_data = []
        
        for year in years:
            for quarter in quarters:
                print(f"Fetching insurance data for {year} Q{quarter}...")
                data = self.get_map_insurance_data(year, quarter)
                if data:
                    df = self.parse_insurance_data(data)
                    if not df.empty:
                        df['Year'] = year
                        df['Quarter'] = quarter
                        all_data.append(df)
        
        if all_data:
            return pd.concat(all_data, ignore_index=True)
        return pd.DataFrame()

