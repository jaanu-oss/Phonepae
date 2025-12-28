"""
Database Insertion Script
Inserts transformed data into MySQL database using batch inserts
"""

import pandas as pd
import logging
from database.db_connection import get_db_connection
import mysql.connector
from mysql.connector import Error

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def insert_aggregated_transactions(df: pd.DataFrame, connection):
    """
    Insert aggregated transaction data into database.
    
    Args:
        df (pd.DataFrame): Transformed transaction DataFrame
        connection: MySQL database connection
    """
    if df.empty:
        logger.warning("No aggregated transaction data to insert")
        return
    
    cursor = connection.cursor()
    
    insert_query = """
    INSERT INTO aggregated_transactions 
    (state, year, quarter, transaction_type, transaction_count, transaction_amount)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    transaction_count = VALUES(transaction_count),
    transaction_amount = VALUES(transaction_amount)
    """
    
    try:
        records = []
        for _, row in df.iterrows():
            records.append((
                row.get('state', ''),
                int(row.get('year', 0)),
                int(row.get('quarter', 0)),
                row.get('transaction_type', ''),
                int(row.get('transaction_count', 0)),
                float(row.get('transaction_amount', 0))
            ))
        
        cursor.executemany(insert_query, records)
        connection.commit()
        logger.info(f"Inserted/Updated {len(records)} aggregated transaction records")
        
    except Error as e:
        logger.error(f"Error inserting aggregated transactions: {e}")
        connection.rollback()
    finally:
        cursor.close()


def insert_aggregated_users(df: pd.DataFrame, connection):
    """
    Insert aggregated user data into database.
    
    Args:
        df (pd.DataFrame): Transformed user DataFrame
        connection: MySQL database connection
    """
    if df.empty:
        logger.warning("No aggregated user data to insert")
        return
    
    cursor = connection.cursor()
    
    insert_query = """
    INSERT INTO aggregated_users 
    (state, year, quarter, registered_users, app_opens)
    VALUES (%s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    registered_users = VALUES(registered_users),
    app_opens = VALUES(app_opens)
    """
    
    try:
        records = []
        for _, row in df.iterrows():
            records.append((
                row.get('state', ''),
                int(row.get('year', 0)),
                int(row.get('quarter', 0)),
                int(row.get('registered_users', 0)),
                int(row.get('app_opens', 0))
            ))
        
        cursor.executemany(insert_query, records)
        connection.commit()
        logger.info(f"Inserted/Updated {len(records)} aggregated user records")
        
    except Error as e:
        logger.error(f"Error inserting aggregated users: {e}")
        connection.rollback()
    finally:
        cursor.close()


def insert_map_transactions(df: pd.DataFrame, connection):
    """
    Insert map transaction data into database.
    
    Args:
        df (pd.DataFrame): Transformed map transaction DataFrame
        connection: MySQL database connection
    """
    if df.empty:
        logger.warning("No map transaction data to insert")
        return
    
    cursor = connection.cursor()
    
    insert_query = """
    INSERT INTO map_transactions 
    (state, year, quarter, district, transaction_count, transaction_amount)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    transaction_count = VALUES(transaction_count),
    transaction_amount = VALUES(transaction_amount)
    """
    
    try:
        records = []
        for _, row in df.iterrows():
            records.append((
                row.get('state', ''),
                int(row.get('year', 0)),
                int(row.get('quarter', 0)),
                row.get('district', ''),
                int(row.get('transaction_count', 0)),
                float(row.get('transaction_amount', 0))
            ))
        
        cursor.executemany(insert_query, records)
        connection.commit()
        logger.info(f"Inserted/Updated {len(records)} map transaction records")
        
    except Error as e:
        logger.error(f"Error inserting map transactions: {e}")
        connection.rollback()
    finally:
        cursor.close()


def insert_map_users(df: pd.DataFrame, connection):
    """
    Insert map user data into database.
    
    Args:
        df (pd.DataFrame): Transformed map user DataFrame
        connection: MySQL database connection
    """
    if df.empty:
        logger.warning("No map user data to insert")
        return
    
    cursor = connection.cursor()
    
    insert_query = """
    INSERT INTO map_users 
    (state, year, quarter, district, registered_users, app_opens)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    registered_users = VALUES(registered_users),
    app_opens = VALUES(app_opens)
    """
    
    try:
        records = []
        for _, row in df.iterrows():
            records.append((
                row.get('state', ''),
                int(row.get('year', 0)),
                int(row.get('quarter', 0)),
                row.get('district', ''),
                int(row.get('registered_users', 0)),
                int(row.get('app_opens', 0))
            ))
        
        cursor.executemany(insert_query, records)
        connection.commit()
        logger.info(f"Inserted/Updated {len(records)} map user records")
        
    except Error as e:
        logger.error(f"Error inserting map users: {e}")
        connection.rollback()
    finally:
        cursor.close()


def insert_top_transactions(df: pd.DataFrame, connection):
    """
    Insert top transaction data into database.
    
    Args:
        df (pd.DataFrame): Transformed top transaction DataFrame
        connection: MySQL database connection
    """
    if df.empty:
        logger.warning("No top transaction data to insert")
        return
    
    cursor = connection.cursor()
    
    insert_query = """
    INSERT INTO top_transactions 
    (state, year, quarter, entity_type, entity_name, transaction_count, transaction_amount)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    transaction_count = VALUES(transaction_count),
    transaction_amount = VALUES(transaction_amount)
    """
    
    try:
        records = []
        for _, row in df.iterrows():
            records.append((
                row.get('state', ''),
                int(row.get('year', 0)),
                int(row.get('quarter', 0)),
                row.get('entity_type', ''),
                str(row.get('entity_name', '')),
                int(row.get('transaction_count', 0)),
                float(row.get('transaction_amount', 0))
            ))
        
        cursor.executemany(insert_query, records)
        connection.commit()
        logger.info(f"Inserted/Updated {len(records)} top transaction records")
        
    except Error as e:
        logger.error(f"Error inserting top transactions: {e}")
        connection.rollback()
    finally:
        cursor.close()


def insert_top_users(df: pd.DataFrame, connection):
    """
    Insert top user data into database.
    
    Args:
        df (pd.DataFrame): Transformed top user DataFrame
        connection: MySQL database connection
    """
    if df.empty:
        logger.warning("No top user data to insert")
        return
    
    cursor = connection.cursor()
    
    insert_query = """
    INSERT INTO top_users 
    (state, year, quarter, entity_type, entity_name, registered_users)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    registered_users = VALUES(registered_users)
    """
    
    try:
        records = []
        for _, row in df.iterrows():
            records.append((
                row.get('state', ''),
                int(row.get('year', 0)),
                int(row.get('quarter', 0)),
                row.get('entity_type', ''),
                str(row.get('entity_name', '')),
                int(row.get('registered_users', 0))
            ))
        
        cursor.executemany(insert_query, records)
        connection.commit()
        logger.info(f"Inserted/Updated {len(records)} top user records")
        
    except Error as e:
        logger.error(f"Error inserting top users: {e}")
        connection.rollback()
    finally:
        cursor.close()


def insert_all_data(transformed_data: dict):
    """
    Insert all transformed data into database.
    
    Args:
        transformed_data (dict): Dictionary of transformed DataFrames
    """
    logger.info("Starting database insertion process...")
    
    try:
        connection = get_db_connection()
        
        if transformed_data.get('aggregated_transactions') is not None:
            insert_aggregated_transactions(transformed_data['aggregated_transactions'], connection)
        
        if transformed_data.get('aggregated_users') is not None:
            insert_aggregated_users(transformed_data['aggregated_users'], connection)
        
        if transformed_data.get('map_transactions') is not None:
            insert_map_transactions(transformed_data['map_transactions'], connection)
        
        if transformed_data.get('map_users') is not None:
            insert_map_users(transformed_data['map_users'], connection)
        
        if transformed_data.get('top_transactions') is not None:
            insert_top_transactions(transformed_data['top_transactions'], connection)
        
        if transformed_data.get('top_users') is not None:
            insert_top_users(transformed_data['top_users'], connection)
        
        logger.info("Database insertion completed successfully!")
        
    except Error as e:
        logger.error(f"Database insertion failed: {e}")
        raise
    finally:
        if connection.is_connected():
            connection.close()
            logger.info("MySQL connection closed")

