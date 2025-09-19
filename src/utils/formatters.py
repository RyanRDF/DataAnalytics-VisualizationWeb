"""
Utility functions for data formatting
"""
import pandas as pd


def format_rupiah(value):
    """Format numeric value to Indonesian Rupiah format (Rp. 1.000.000)"""
    if pd.isna(value) or value == 0 or value == '' or value is None:
        return "Rp. 0"
    
    try:
        # Convert to integer to remove decimals
        int_value = int(float(value))
        
        # Format with thousand separators
        formatted = f"{int_value:,}".replace(",", ".")
        
        return f"Rp. {formatted}"
    except (ValueError, TypeError):
        return "Rp. 0"


def format_number(value, decimal_places=0):
    """Format numeric value with thousand separators"""
    if pd.isna(value) or value == 0 or value == '' or value is None:
        return "0"
    
    try:
        if decimal_places > 0:
            formatted = f"{float(value):,.{decimal_places}f}".replace(",", ".")
        else:
            int_value = int(float(value))
            formatted = f"{int_value:,}".replace(",", ".")
        
        return formatted
    except (ValueError, TypeError):
        return "0"


def format_percentage(value, decimal_places=1):
    """Format numeric value as percentage"""
    if pd.isna(value) or value == 0 or value == '' or value is None:
        return "0%"
    
    try:
        percentage = float(value) * 100
        formatted = f"{percentage:,.{decimal_places}f}%".replace(",", ".")
        return formatted
    except (ValueError, TypeError):
        return "0%"
