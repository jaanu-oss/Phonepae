"""
View Stored Data from MySQL Database
Simple script to query and display data from all tables
"""

import sys
from pathlib import Path
import pandas as pd

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from database.db_connection import get_db_connection


def view_table_data(table_name, limit=10):
    """
    View data from a specific table.
    
    Args:
        table_name (str): Name of the table to query
        limit (int): Number of records to display (default: 10)
    """
    connection = None
    try:
        connection = get_db_connection()
        
        # Get total count
        count_query = f"SELECT COUNT(*) as total FROM {table_name}"
        count_df = pd.read_sql(count_query, connection)
        total_records = count_df['total'].iloc[0]
        
        print(f"\n{'='*80}")
        print(f"Table: {table_name}")
        print(f"Total Records: {total_records}")
        print(f"{'='*80}")
        
        if total_records == 0:
            print("No data found in this table.")
            return
        
        # Get sample data
        query = f"SELECT * FROM {table_name} LIMIT {limit}"
        df = pd.read_sql(query, connection)
        
        # Display data
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', 50)
        
        print(f"\nShowing first {min(limit, total_records)} records:\n")
        print(df.to_string(index=False))
        
        if total_records > limit:
            print(f"\n... and {total_records - limit} more records (use --limit to see more)")
        
    except Exception as e:
        print(f"Error viewing table {table_name}: {e}")
    finally:
        if connection and connection.is_connected():
            connection.close()


def view_all_tables_summary():
    """Display summary of all tables."""
    connection = None
    try:
        connection = get_db_connection()
        
        tables = [
            'aggregated_transactions',
            'aggregated_users',
            'map_transactions',
            'map_users',
            'top_transactions',
            'top_users'
        ]
        
        print("\n" + "="*80)
        print("DATABASE SUMMARY")
        print("="*80)
        
        summary_data = []
        for table in tables:
            try:
                query = f"SELECT COUNT(*) as count FROM {table}"
                df = pd.read_sql(query, connection)
                count = df['count'].iloc[0]
                summary_data.append({'Table': table, 'Records': count})
            except Exception as e:
                summary_data.append({'Table': table, 'Records': f'Error: {e}'})
        
        summary_df = pd.DataFrame(summary_data)
        print("\n")
        print(summary_df.to_string(index=False))
        print("\n" + "="*80)
        
    except Exception as e:
        print(f"Error getting summary: {e}")
    finally:
        if connection and connection.is_connected():
            connection.close()


def view_custom_query(query):
    """Execute and display results of a custom SQL query."""
    connection = None
    try:
        connection = get_db_connection()
        df = pd.read_sql(query, connection)
        
        print(f"\n{'='*80}")
        print("Query Results")
        print(f"{'='*80}\n")
        print(f"Rows returned: {len(df)}")
        print("\n")
        
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', 50)
        
        print(df.to_string(index=False))
        
    except Exception as e:
        print(f"Error executing query: {e}")
    finally:
        if connection and connection.is_connected():
            connection.close()


def main():
    """Main function to handle command line arguments."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='View data from PhonePe Pulse MySQL database',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python view_data.py                          # Show summary of all tables
  python view_data.py --table aggregated_transactions
  python view_data.py --table aggregated_transactions --limit 20
  python view_data.py --query "SELECT * FROM aggregated_transactions WHERE year=2023 LIMIT 5"
        """
    )
    
    parser.add_argument(
        '--table',
        type=str,
        help='Name of the table to view (aggregated_transactions, aggregated_users, map_transactions, map_users, top_transactions, top_users)'
    )
    
    parser.add_argument(
        '--limit',
        type=int,
        default=10,
        help='Number of records to display (default: 10)'
    )
    
    parser.add_argument(
        '--query',
        type=str,
        help='Custom SQL query to execute'
    )
    
    parser.add_argument(
        '--all',
        action='store_true',
        help='Show all tables with sample data'
    )
    
    args = parser.parse_args()
    
    # If custom query provided
    if args.query:
        view_custom_query(args.query)
        return
    
    # If specific table provided
    if args.table:
        view_table_data(args.table, args.limit)
        return
    
    # If --all flag
    if args.all:
        view_all_tables_summary()
        print("\n")
        tables = [
            'aggregated_transactions',
            'aggregated_users',
            'map_transactions',
            'map_users',
            'top_transactions',
            'top_users'
        ]
        for table in tables:
            view_table_data(table, args.limit)
        return
    
    # Default: show summary
    view_all_tables_summary()
    print("\n💡 Tip: Use --table <table_name> to view specific table data")
    print("   Use --all to view all tables")
    print("   Use --query 'SELECT ...' to run custom SQL queries")


if __name__ == "__main__":
    main()

