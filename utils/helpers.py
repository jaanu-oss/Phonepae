"""
Helper utility functions for data processing
"""

import json
import os
import logging
from typing import Dict, List, Any
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def normalize_state_name(state_name: str) -> str:
    """
    Normalize state names to consistent format.
    
    Args:
        state_name (str): Raw state name
        
    Returns:
        str: Normalized state name (title case)
    """
    if not state_name:
        return ""
    
    # Convert to lowercase and remove extra spaces
    normalized = state_name.lower().strip()
    
    # Handle special cases
    state_mappings = {
        'andaman & nicobar islands': 'andaman and nicobar islands',
        'dadra & nagar haveli & daman & diu': 'dadra and nagar haveli and daman and diu',
        'jammu & kashmir': 'jammu and kashmir'
    }
    
    normalized = state_mappings.get(normalized, normalized)
    
    # Convert to title case
    return normalized.title()


def extract_year_quarter(file_path: str) -> tuple:
    """
    Extract year and quarter from file path.
    
    Args:
        file_path (str): Path to JSON file
        
    Returns:
        tuple: (year, quarter) or (None, None) if not found
    """
    try:
        # Pattern: /year/quarter.json or /year/quarter/
        parts = file_path.replace('\\', '/').split('/')
        
        year = None
        quarter = None
        
        for i, part in enumerate(parts):
            # Check if part is a year (4 digits, 2018-2024)
            if part.isdigit() and len(part) == 4 and 2018 <= int(part) <= 2024:
                year = int(part)
                # Check if next part is quarter
                if i + 1 < len(parts):
                    next_part = parts[i + 1].replace('.json', '').replace('\\', '')
                    if next_part.isdigit() and 1 <= int(next_part) <= 4:
                        quarter = int(next_part)
                        break
        
        return year, quarter
    except Exception as e:
        logger.warning(f"Error extracting year/quarter from {file_path}: {e}")
        return None, None


def load_json_file(file_path: str) -> Dict:
    """
    Load JSON file and return parsed data.
    
    Args:
        file_path (str): Path to JSON file
        
    Returns:
        dict: Parsed JSON data
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading JSON file {file_path}: {e}")
        return {}


def find_json_files(directory: str, pattern: str = None) -> List[str]:
    """
    Find all JSON files in a directory recursively.
    
    Args:
        directory (str): Root directory to search
        pattern (str): Optional pattern to filter files
        
    Returns:
        list: List of JSON file paths
    """
    json_files = []
    
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    if pattern is None or pattern in file_path:
                        json_files.append(file_path)
    except Exception as e:
        logger.error(f"Error finding JSON files: {e}")
    
    return json_files


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers, returning default if denominator is zero.
    
    Args:
        numerator (float): Numerator
        denominator (float): Denominator
        default (float): Default value if division by zero
        
    Returns:
        float: Result of division or default
    """
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except (TypeError, ValueError):
        return default


def format_number(num: float) -> str:
    """
    Format large numbers with K, M, B suffixes.
    
    Args:
        num (float): Number to format
        
    Returns:
        str: Formatted string
    """
    try:
        num = float(num)
        if num >= 1e9:
            return f"{num/1e9:.2f}B"
        elif num >= 1e6:
            return f"{num/1e6:.2f}M"
        elif num >= 1e3:
            return f"{num/1e3:.2f}K"
        else:
            return f"{num:.2f}"
    except (TypeError, ValueError):
        return "0"


def clean_string(text: str) -> str:
    """
    Clean string by removing extra spaces and special characters.
    
    Args:
        text (str): Input string
        
    Returns:
        str: Cleaned string
    """
    if not text:
        return ""
    
    # Remove extra spaces
    cleaned = ' '.join(text.split())
    
    # Remove special characters except spaces and hyphens
    cleaned = re.sub(r'[^\w\s-]', '', cleaned)
    
    return cleaned.strip()

