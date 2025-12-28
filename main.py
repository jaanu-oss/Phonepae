"""
Main Orchestrator Script
Coordinates the entire ETL pipeline: Clone → Extract → Transform → Load
"""

import os
import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from scripts.clone_repo import clone_repository
from scripts.extract_data import extract_all_data
from scripts.transform_data import transform_all_data
from database.insert_data import insert_all_data
from database.db_connection import create_database_if_not_exists, execute_sql_file

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('etl_pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def setup_database():
    """
    Setup database schema.
    """
    try:
        logger.info("Setting up database...")
        create_database_if_not_exists()
        
        schema_file = os.path.join("database", "schema.sql")
        if os.path.exists(schema_file):
            execute_sql_file(schema_file)
            logger.info("Database schema created successfully!")
        else:
            logger.warning(f"Schema file not found: {schema_file}")
    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        raise


def run_etl_pipeline():
    """
    Run the complete ETL pipeline.
    """
    try:
        logger.info("=" * 60)
        logger.info("Starting PhonePe Pulse ETL Pipeline")
        logger.info("=" * 60)
        
        # Step 1: Setup Database
        logger.info("\n[Step 1/4] Setting up database...")
        setup_database()
        
        # Step 2: Clone Repository
        logger.info("\n[Step 2/4] Cloning PhonePe Pulse repository...")
        if not clone_repository():
            raise Exception("Repository cloning failed!")
        
        # Step 3: Extract Data
        logger.info("\n[Step 3/4] Extracting data from repository...")
        extracted_data = extract_all_data()
        
        if not extracted_data or sum(len(v) for v in extracted_data.values() if v) == 0:
            raise Exception("No data extracted from repository!")
        
        # Step 4: Transform Data
        logger.info("\n[Step 4/4] Transforming data...")
        transformed_data = transform_all_data(extracted_data)
        
        # Step 5: Load Data into Database
        logger.info("\n[Step 5/5] Loading data into MySQL database...")
        insert_all_data(transformed_data)
        
        logger.info("\n" + "=" * 60)
        logger.info("ETL Pipeline Completed Successfully!")
        logger.info("=" * 60)
        
        # Print summary
        logger.info("\nData Summary:")
        for table_name, df in transformed_data.items():
            if df is not None and not df.empty:
                logger.info(f"  {table_name}: {len(df)} records")
        
        logger.info("\nNext Steps:")
        logger.info("1. Update .env file with your MySQL credentials")
        logger.info("2. Run the Streamlit dashboard: streamlit run dashboard/app.py")
        
    except Exception as e:
        logger.error(f"\nETL Pipeline failed: {e}")
        logger.exception("Full error traceback:")
        sys.exit(1)


if __name__ == "__main__":
    run_etl_pipeline()

