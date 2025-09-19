"""
Utility functions for data validation
"""
import pandas as pd
from typing import List, Tuple, Optional


def validate_required_columns(df: pd.DataFrame, required_columns: List[str]) -> Tuple[bool, Optional[str]]:
    """
    Validate if all required columns exist in the dataframe
    
    Args:
        df: DataFrame to validate
        required_columns: List of required column names
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if df is None:
        return False, "No data available. Please upload a file first."
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return False, f"Missing columns: {', '.join(missing_columns)}"
    
    return True, None


def validate_date_range(start_date: Optional[str], end_date: Optional[str]) -> Tuple[bool, Optional[str]]:
    """
    Validate date range parameters
    
    Args:
        start_date: Start date string (YYYY-MM-DD format)
        end_date: End date string (YYYY-MM-DD format)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if start_date and end_date:
        try:
            from datetime import datetime
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            
            if start_dt > end_dt:
                return False, "Start date cannot be later than end date"
        except ValueError:
            return False, "Invalid date format. Use YYYY-MM-DD"
    
    return True, None


def validate_sort_parameters(sort_column: Optional[str], available_columns: List[str]) -> Tuple[bool, Optional[str]]:
    """
    Validate sorting parameters
    
    Args:
        sort_column: Column name to sort by
        available_columns: List of available column names
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if sort_column and sort_column not in available_columns:
        return False, f"Invalid sort column: {sort_column}. Available columns: {', '.join(available_columns)}"
    
    return True, None
