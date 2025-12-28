"""
Data Transformation Script
Cleans, normalizes, and transforms extracted data using Pandas
"""

import pandas as pd
import logging
from utils.helpers import normalize_state_name, clean_string

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def transform_aggregated_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform aggregated transaction data.
    
    Args:
        df (pd.DataFrame): Raw transaction DataFrame
        
    Returns:
        pd.DataFrame: Transformed DataFrame
    """
    if df.empty:
        return df
    
    # Create a copy
    df = df.copy()
    
    # Normalize state names
    if 'state' in df.columns:
        df['state'] = df['state'].apply(normalize_state_name)
    
    # Clean transaction type
    if 'transaction_type' in df.columns:
        df['transaction_type'] = df['transaction_type'].apply(clean_string)
    
    # Ensure numeric columns are correct types
    numeric_columns = ['transaction_count', 'transaction_amount', 'year', 'quarter']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Aggregate by state, year, quarter, transaction_type (sum payment modes if present)
    groupby_cols = ['state', 'year', 'quarter', 'transaction_type']
    if 'payment_mode' in df.columns:
        # Group and sum if payment_mode column exists
        df = df.groupby(groupby_cols).agg({
            'transaction_count': 'sum',
            'transaction_amount': 'sum'
        }).reset_index()
    else:
        # If no payment_mode, data is already aggregated or needs grouping
        df = df.groupby(groupby_cols).agg({
            'transaction_count': 'sum',
            'transaction_amount': 'sum'
        }).reset_index()
    
    # Remove nulls
    df = df.dropna(subset=['state', 'year', 'quarter', 'transaction_type'])
    
    logger.info(f"Transformed {len(df)} aggregated transaction records")
    return df


def transform_aggregated_users(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform aggregated user data.
    
    Args:
        df (pd.DataFrame): Raw user DataFrame
        
    Returns:
        pd.DataFrame: Transformed DataFrame
    """
    if df.empty:
        return df
    
    # Create a copy
    df = df.copy()
    
    # Normalize state names
    if 'state' in df.columns:
        df['state'] = df['state'].apply(normalize_state_name)
    
    # Ensure numeric columns are correct types
    numeric_columns = ['registered_users', 'app_opens', 'year', 'quarter']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Remove nulls
    df = df.dropna(subset=['state', 'year', 'quarter'])
    
    logger.info(f"Transformed {len(df)} aggregated user records")
    return df


def transform_map_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform map transaction data.
    
    Args:
        df (pd.DataFrame): Raw map transaction DataFrame
        
    Returns:
        pd.DataFrame: Transformed DataFrame
    """
    if df.empty:
        return df
    
    # Create a copy
    df = df.copy()
    
    # Normalize state and district names
    if 'state' in df.columns:
        df['state'] = df['state'].apply(normalize_state_name)
    if 'district' in df.columns:
        df['district'] = df['district'].apply(clean_string)
    
    # Ensure numeric columns are correct types
    numeric_columns = ['transaction_count', 'transaction_amount', 'year', 'quarter']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Remove nulls
    df = df.dropna(subset=['state', 'year', 'quarter'])
    
    logger.info(f"Transformed {len(df)} map transaction records")
    return df


def transform_map_users(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform map user data.
    
    Args:
        df (pd.DataFrame): Raw map user DataFrame
        
    Returns:
        pd.DataFrame: Transformed DataFrame
    """
    if df.empty:
        return df
    
    # Create a copy
    df = df.copy()
    
    # Normalize state and district names
    if 'state' in df.columns:
        df['state'] = df['state'].apply(normalize_state_name)
    if 'district' in df.columns:
        df['district'] = df['district'].apply(clean_string)
    
    # Ensure numeric columns are correct types
    numeric_columns = ['registered_users', 'app_opens', 'year', 'quarter']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Remove nulls
    df = df.dropna(subset=['state', 'year', 'quarter'])
    
    logger.info(f"Transformed {len(df)} map user records")
    return df


def transform_top_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform top transaction data.
    
    Args:
        df (pd.DataFrame): Raw top transaction DataFrame
        
    Returns:
        pd.DataFrame: Transformed DataFrame
    """
    if df.empty:
        return df
    
    # Create a copy
    df = df.copy()
    
    # Normalize state and entity names
    if 'state' in df.columns:
        df['state'] = df['state'].apply(normalize_state_name)
    if 'entity_name' in df.columns:
        df['entity_name'] = df['entity_name'].apply(clean_string)
    
    # Clean entity type
    if 'entity_type' in df.columns:
        df['entity_type'] = df['entity_type'].str.lower()
    
    # Ensure numeric columns are correct types
    numeric_columns = ['transaction_count', 'transaction_amount', 'year', 'quarter']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Remove nulls
    df = df.dropna(subset=['state', 'year', 'quarter', 'entity_type', 'entity_name'])
    
    logger.info(f"Transformed {len(df)} top transaction records")
    return df


def transform_top_users(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform top user data.
    
    Args:
        df (pd.DataFrame): Raw top user DataFrame
        
    Returns:
        pd.DataFrame: Transformed DataFrame
    """
    if df.empty:
        return df
    
    # Create a copy
    df = df.copy()
    
    # Normalize state and entity names
    if 'state' in df.columns:
        df['state'] = df['state'].apply(normalize_state_name)
    if 'entity_name' in df.columns:
        df['entity_name'] = df['entity_name'].apply(clean_string)
    
    # Clean entity type
    if 'entity_type' in df.columns:
        df['entity_type'] = df['entity_type'].str.lower()
    
    # Ensure numeric columns are correct types
    numeric_columns = ['registered_users', 'year', 'quarter']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Remove nulls
    df = df.dropna(subset=['state', 'year', 'quarter', 'entity_type', 'entity_name'])
    
    logger.info(f"Transformed {len(df)} top user records")
    return df


def transform_all_data(extracted_data: dict) -> dict:
    """
    Transform all extracted data.
    
    Args:
        extracted_data (dict): Dictionary of extracted DataFrames
        
    Returns:
        dict: Dictionary of transformed DataFrames
    """
    logger.info("Starting data transformation process...")
    
    transformed_data = {}
    
    # Convert lists to DataFrames and transform
    if extracted_data.get('aggregated_transactions'):
        df = pd.DataFrame(extracted_data['aggregated_transactions'])
        transformed_data['aggregated_transactions'] = transform_aggregated_transactions(df)
    
    if extracted_data.get('aggregated_users'):
        df = pd.DataFrame(extracted_data['aggregated_users'])
        transformed_data['aggregated_users'] = transform_aggregated_users(df)
    
    if extracted_data.get('map_transactions'):
        df = pd.DataFrame(extracted_data['map_transactions'])
        transformed_data['map_transactions'] = transform_map_transactions(df)
    
    if extracted_data.get('map_users'):
        df = pd.DataFrame(extracted_data['map_users'])
        transformed_data['map_users'] = transform_map_users(df)
    
    if extracted_data.get('top_transactions'):
        df = pd.DataFrame(extracted_data['top_transactions'])
        transformed_data['top_transactions'] = transform_top_transactions(df)
    
    if extracted_data.get('top_users'):
        df = pd.DataFrame(extracted_data['top_users'])
        transformed_data['top_users'] = transform_top_users(df)
    
    logger.info("Data transformation completed!")
    return transformed_data

