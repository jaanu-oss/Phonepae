"""
Database Connection Module
Handles MySQL database connections using mysql-connector-python
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_db_connection():
    """
    Create and return a MySQL database connection.
    
    Returns:
        mysql.connector.connection.MySQLConnection: Database connection object
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'phonepe_pulse'),
            port=int(os.getenv('DB_PORT', 3306)),
            autocommit=False
        )
        
        if connection.is_connected():
            logger.info("Successfully connected to MySQL database")
            return connection
            
    except Error as e:
        logger.error(f"Error connecting to MySQL database: {e}")
        raise


def create_database_if_not_exists():
    """
    Create the database if it doesn't exist.
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            port=int(os.getenv('DB_PORT', 3306))
        )
        
        cursor = connection.cursor()
        db_name = os.getenv('DB_NAME', 'phonepe_pulse')
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        logger.info(f"Database '{db_name}' created or already exists")
        cursor.close()
        connection.close()
        
    except Error as e:
        logger.error(f"Error creating database: {e}")
        raise


def execute_sql_file(sql_file_path):
    """
    Execute SQL statements from a file.
    
    Args:
        sql_file_path (str): Path to the SQL file
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'phonepe_pulse'),
            port=int(os.getenv('DB_PORT', 3306))
        )
        
        cursor = connection.cursor()
        
        with open(sql_file_path, 'r', encoding='utf-8') as file:
            sql_script = file.read()
            
        # Execute multiple statements
        for statement in sql_script.split(';'):
            if statement.strip():
                cursor.execute(statement)
        
        connection.commit()
        logger.info(f"SQL file '{sql_file_path}' executed successfully")
        cursor.close()
        connection.close()
        
    except Error as e:
        logger.error(f"Error executing SQL file: {e}")
        if connection.is_connected():
            connection.rollback()
        raise

