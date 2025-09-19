"""
Utility functions for data processing
"""
import pandas as pd
from typing import List, Optional, Tuple
from datetime import datetime


def apply_date_filter(df: pd.DataFrame, start_date: Optional[str], end_date: Optional[str], date_column: str = 'ADMISSION_DATE') -> pd.DataFrame:
    """
    Apply date range filter to dataframe
    
    Args:
        df: DataFrame to filter
        start_date: Start date string (YYYY-MM-DD format)
        end_date: End date string (YYYY-MM-DD format)
        date_column: Name of the date column to filter by
        
    Returns:
        Filtered DataFrame
    """
    if not start_date and not end_date:
        return df
    
    # Convert date column to datetime if it's not already
    if date_column in df.columns:
        df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
        
        if start_date:
            start_dt = pd.to_datetime(start_date)
            df = df[df[date_column] >= start_dt]
        
        if end_date:
            end_dt = pd.to_datetime(end_date)
            df = df[df[date_column] <= end_dt]
    
    return df


def apply_sorting(df: pd.DataFrame, sort_column: Optional[str], sort_order: str = 'ASC') -> pd.DataFrame:
    """
    Apply sorting to dataframe
    
    Args:
        df: DataFrame to sort
        sort_column: Column name to sort by
        sort_order: Sort order ('ASC' or 'DESC')
        
    Returns:
        Sorted DataFrame
    """
    if not sort_column or sort_column not in df.columns:
        return df
    
    ascending = sort_order.upper() == 'ASC'
    return df.sort_values(by=sort_column, ascending=ascending)


def apply_specific_filter(df: pd.DataFrame, filter_column: str, filter_value: str) -> pd.DataFrame:
    """
    Apply specific column value filter to dataframe
    
    Args:
        df: DataFrame to filter
        filter_column: Column name to filter by
        filter_value: Value to filter for
        
    Returns:
        Filtered DataFrame
    """
    if not filter_column or filter_column not in df.columns:
        return df
    
    # Convert filter value to string for comparison
    filter_value_str = str(filter_value).lower()
    
    # Apply case-insensitive filter
    mask = df[filter_column].astype(str).str.lower().str.contains(filter_value_str, na=False)
    return df[mask]


def safe_numeric_conversion(series: pd.Series, fill_value: float = 0) -> pd.Series:
    """
    Safely convert series to numeric with error handling
    
    Args:
        series: Pandas Series to convert
        fill_value: Value to use for non-numeric entries
        
    Returns:
        Numeric Series
    """
    return pd.to_numeric(series, errors='coerce').fillna(fill_value)


def extract_diagnosis_codes(diaglist: str) -> Tuple[str, str]:
    """
    Extract PDX and SDX from diagnosis list
    
    Args:
        diaglist: Diagnosis list string
        
    Returns:
        Tuple of (PDX, SDX)
    """
    if pd.isna(diaglist) or diaglist == '':
        return '', ''
    
    diaglist_str = str(diaglist)
    if ';' in diaglist_str:
        parts = diaglist_str.split(';')
        pdx = parts[0].strip() if len(parts) > 0 else ''
        sdx = '; '.join(parts[1:]).strip() if len(parts) > 1 else ''
        return pdx, sdx
    else:
        return diaglist_str.strip(), ''


def calculate_age_in_days(birth_date: str, admission_date: str) -> int:
    """
    Calculate age in days from birth date and admission date
    
    Args:
        birth_date: Birth date string
        admission_date: Admission date string
        
    Returns:
        Age in days
    """
    try:
        birth_dt = pd.to_datetime(birth_date, errors='coerce')
        admission_dt = pd.to_datetime(admission_date, errors='coerce')
        
        if pd.isna(birth_dt) or pd.isna(admission_dt):
            return 0
        
        age_days = (admission_dt - birth_dt).days
        return max(0, age_days)
    except:
        return 0
