"""
Data Extraction Script
Extracts JSON data from the cloned PhonePe Pulse repository
"""

import os
import json
import logging
from pathlib import Path
from utils.helpers import load_json_file, find_json_files, extract_year_quarter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

REPO_DATA_DIR = os.path.join("data", "raw", "pulse", "data")
EXTRACTED_DATA_DIR = os.path.join("data", "processed")


def extract_aggregated_transactions():
    """
    Extract aggregated transaction data.
    
    Returns:
        list: List of transaction records
    """
    records = []
    base_path = os.path.join(REPO_DATA_DIR, "aggregated", "transaction", "country", "india")
    
    if not os.path.exists(base_path):
        logger.warning(f"Path not found: {base_path}")
        return records
    
    json_files = find_json_files(base_path)
    logger.info(f"Found {len(json_files)} aggregated transaction files")
    
    for file_path in json_files:
        year, quarter = extract_year_quarter(file_path)
        if not year or not quarter:
            continue
            
        data = load_json_file(file_path)
        
        if not data.get('success') or not data.get('data'):
            continue
            
        transaction_data = data.get('data', {}).get('transactionData', [])
        
        for item in transaction_data:
            transaction_type = item.get('name', '')
            payment_modes = item.get('paymentInstruments', [])
            
            for payment_mode in payment_modes:
                records.append({
                    'state': 'india',
                    'year': year,
                    'quarter': quarter,
                    'transaction_type': transaction_type,
                    'payment_mode': payment_mode.get('type', ''),
                    'transaction_count': payment_mode.get('count', 0),
                    'transaction_amount': payment_mode.get('amount', 0)
                })
    
    logger.info(f"Extracted {len(records)} aggregated transaction records")
    return records


def extract_aggregated_users():
    """
    Extract aggregated user data.
    
    Returns:
        list: List of user records
    """
    records = []
    base_path = os.path.join(REPO_DATA_DIR, "aggregated", "user", "country", "india")
    
    if not os.path.exists(base_path):
        logger.warning(f"Path not found: {base_path}")
        return records
    
    json_files = find_json_files(base_path)
    logger.info(f"Found {len(json_files)} aggregated user files")
    
    for file_path in json_files:
        year, quarter = extract_year_quarter(file_path)
        if not year or not quarter:
            continue
            
        data = load_json_file(file_path)
        
        if not data.get('success') or not data.get('data'):
            continue
            
        user_data = data.get('data', {}).get('aggregated', {})
        
        records.append({
            'state': 'india',
            'year': year,
            'quarter': quarter,
            'registered_users': user_data.get('registeredUsers', 0),
            'app_opens': user_data.get('appOpens', 0)
        })
    
    logger.info(f"Extracted {len(records)} aggregated user records")
    return records


def extract_map_transactions():
    """
    Extract map transaction data (state and district level).
    
    Returns:
        list: List of map transaction records
    """
    records = []
    base_path = os.path.join(REPO_DATA_DIR, "map", "transaction", "hover", "country", "india")
    
    # Extract country level (state data)
    if os.path.exists(base_path):
        json_files = find_json_files(base_path)
        logger.info(f"Found {len(json_files)} map transaction (country) files")
        
        for file_path in json_files:
            year, quarter = extract_year_quarter(file_path)
            if not year or not quarter:
                continue
                
            data = load_json_file(file_path)
            
            if not data.get('success') or not data.get('data'):
                continue
                
            hover_data = data.get('data', {}).get('hoverDataList', [])
            
            for item in hover_data:
                state_name = item.get('name', '').lower()
                metrics = item.get('metric', [])
                
                for metric in metrics:
                    records.append({
                        'state': state_name,
                        'year': year,
                        'quarter': quarter,
                        'district': state_name,  # At country level, district = state
                        'transaction_count': metric.get('count', 0),
                        'transaction_amount': metric.get('amount', 0)
                    })
    
    # Extract state level (district data)
    state_base = os.path.join(REPO_DATA_DIR, "map", "transaction", "hover", "country", "india", "state")
    if os.path.exists(state_base):
        for state_dir in os.listdir(state_base):
            state_path = os.path.join(state_base, state_dir)
            if not os.path.isdir(state_path):
                continue
                
            json_files = find_json_files(state_path)
            
            for file_path in json_files:
                year, quarter = extract_year_quarter(file_path)
                if not year or not quarter:
                    continue
                    
                data = load_json_file(file_path)
                
                if not data.get('success') or not data.get('data'):
                    continue
                    
                hover_data = data.get('data', {}).get('hoverDataList', [])
                
                for item in hover_data:
                    district_name = item.get('name', '').lower()
                    metrics = item.get('metric', [])
                    
                    for metric in metrics:
                        records.append({
                            'state': state_dir.lower(),
                            'year': year,
                            'quarter': quarter,
                            'district': district_name,
                            'transaction_count': metric.get('count', 0),
                            'transaction_amount': metric.get('amount', 0)
                        })
    
    logger.info(f"Extracted {len(records)} map transaction records")
    return records


def extract_map_users():
    """
    Extract map user data (state and district level).
    
    Returns:
        list: List of map user records
    """
    records = []
    base_path = os.path.join(REPO_DATA_DIR, "map", "user", "hover", "country", "india")
    
    # Extract country level (state data)
    if os.path.exists(base_path):
        json_files = find_json_files(base_path)
        logger.info(f"Found {len(json_files)} map user (country) files")
        
        for file_path in json_files:
            year, quarter = extract_year_quarter(file_path)
            if not year or not quarter:
                continue
                
            data = load_json_file(file_path)
            
            if not data.get('success') or not data.get('data'):
                continue
                
            hover_data = data.get('data', {}).get('hoverData', {})
            
            for state_name, state_data in hover_data.items():
                records.append({
                    'state': state_name.lower(),
                    'year': year,
                    'quarter': quarter,
                    'district': state_name.lower(),  # At country level, district = state
                    'registered_users': state_data.get('registeredUsers', 0),
                    'app_opens': state_data.get('appOpens', 0)
                })
    
    # Extract state level (district data)
    state_base = os.path.join(REPO_DATA_DIR, "map", "user", "hover", "country", "india", "state")
    if os.path.exists(state_base):
        for state_dir in os.listdir(state_base):
            state_path = os.path.join(state_base, state_dir)
            if not os.path.isdir(state_path):
                continue
                
            json_files = find_json_files(state_path)
            
            for file_path in json_files:
                year, quarter = extract_year_quarter(file_path)
                if not year or not quarter:
                    continue
                    
                data = load_json_file(file_path)
                
                if not data.get('success') or not data.get('data'):
                    continue
                    
                hover_data = data.get('data', {}).get('hoverData', {})
                
                for district_name, district_data in hover_data.items():
                    records.append({
                        'state': state_dir.lower(),
                        'year': year,
                        'quarter': quarter,
                        'district': district_name.lower(),
                        'registered_users': district_data.get('registeredUsers', 0),
                        'app_opens': district_data.get('appOpens', 0)
                    })
    
    logger.info(f"Extracted {len(records)} map user records")
    return records


def extract_top_transactions():
    """
    Extract top transaction data.
    
    Returns:
        list: List of top transaction records
    """
    records = []
    base_path = os.path.join(REPO_DATA_DIR, "top", "transaction", "country", "india")
    
    if not os.path.exists(base_path):
        logger.warning(f"Path not found: {base_path}")
        return records
    
    json_files = find_json_files(base_path)
    logger.info(f"Found {len(json_files)} top transaction files")
    
    for file_path in json_files:
        year, quarter = extract_year_quarter(file_path)
        if not year or not quarter:
            continue
            
        data = load_json_file(file_path)
        
        if not data.get('success') or not data.get('data'):
            continue
            
        data_obj = data.get('data', {})
        if not data_obj:
            continue
        
        # Extract states
        states = data_obj.get('states', []) or []
        for item in states:
            if not item:
                continue
            entity_name = item.get('entityName', '')
            metric = item.get('metric', {})
            
            records.append({
                'state': 'india',
                'year': year,
                'quarter': quarter,
                'entity_type': 'state',
                'entity_name': entity_name.lower(),
                'transaction_count': metric.get('count', 0),
                'transaction_amount': metric.get('amount', 0)
            })
        
        # Extract districts
        districts = data_obj.get('districts', []) or []
        for item in districts:
            if not item:
                continue
            entity_name = item.get('entityName', '')
            metric = item.get('metric', {})
            
            records.append({
                'state': 'india',
                'year': year,
                'quarter': quarter,
                'entity_type': 'district',
                'entity_name': entity_name.lower(),
                'transaction_count': metric.get('count', 0),
                'transaction_amount': metric.get('amount', 0)
            })
        
        # Extract pincodes
        pincodes = data_obj.get('pincodes', []) or []
        for item in pincodes:
            if not item:
                continue
            entity_name = item.get('entityName', '')
            metric = item.get('metric', {})
            
            records.append({
                'state': 'india',
                'year': year,
                'quarter': quarter,
                'entity_type': 'pincode',
                'entity_name': str(entity_name),
                'transaction_count': metric.get('count', 0),
                'transaction_amount': metric.get('amount', 0)
            })
    
    logger.info(f"Extracted {len(records)} top transaction records")
    return records


def extract_top_users():
    """
    Extract top user data.
    
    Returns:
        list: List of top user records
    """
    records = []
    base_path = os.path.join(REPO_DATA_DIR, "top", "user", "country", "india")
    
    if not os.path.exists(base_path):
        logger.warning(f"Path not found: {base_path}")
        return records
    
    json_files = find_json_files(base_path)
    logger.info(f"Found {len(json_files)} top user files")
    
    for file_path in json_files:
        year, quarter = extract_year_quarter(file_path)
        if not year or not quarter:
            continue
            
        data = load_json_file(file_path)
        
        if not data.get('success') or not data.get('data'):
            continue
            
        data_obj = data.get('data', {})
        if not data_obj:
            continue
        
        # Extract states
        states = data_obj.get('states', []) or []
        for item in states:
            if not item:
                continue
            records.append({
                'state': 'india',
                'year': year,
                'quarter': quarter,
                'entity_type': 'state',
                'entity_name': item.get('name', '').lower(),
                'registered_users': item.get('registeredUsers', 0)
            })
        
        # Extract districts
        districts = data_obj.get('districts', []) or []
        for item in districts:
            if not item:
                continue
            records.append({
                'state': 'india',
                'year': year,
                'quarter': quarter,
                'entity_type': 'district',
                'entity_name': item.get('name', '').lower(),
                'registered_users': item.get('registeredUsers', 0)
            })
        
        # Extract pincodes
        pincodes = data_obj.get('pincodes', []) or []
        for item in pincodes:
            if not item:
                continue
            records.append({
                'state': 'india',
                'year': year,
                'quarter': quarter,
                'entity_type': 'pincode',
                'entity_name': str(item.get('name', '')),
                'registered_users': item.get('registeredUsers', 0)
            })
    
    logger.info(f"Extracted {len(records)} top user records")
    return records


def extract_all_data():
    """
    Extract all data types from the repository.
    
    Returns:
        dict: Dictionary containing all extracted data
    """
    logger.info("Starting data extraction process...")
    
    # Create processed directory
    Path(EXTRACTED_DATA_DIR).mkdir(parents=True, exist_ok=True)
    
    extracted_data = {
        'aggregated_transactions': extract_aggregated_transactions(),
        'aggregated_users': extract_aggregated_users(),
        'map_transactions': extract_map_transactions(),
        'map_users': extract_map_users(),
        'top_transactions': extract_top_transactions(),
        'top_users': extract_top_users()
    }
    
    # Save extracted data as JSON for backup
    output_file = os.path.join(EXTRACTED_DATA_DIR, "extracted_data_summary.json")
    summary = {k: len(v) for k, v in extracted_data.items()}
    
    with open(output_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    logger.info(f"Data extraction completed. Summary saved to {output_file}")
    logger.info(f"Total records extracted: {sum(len(v) for v in extracted_data.values())}")
    
    return extracted_data


if __name__ == "__main__":
    extracted_data = extract_all_data()
    logger.info("Data extraction process completed!")

