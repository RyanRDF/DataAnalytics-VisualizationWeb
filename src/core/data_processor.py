"""
Data processor for INACBG-based pricing adjustments
"""
import pandas as pd
import numpy as np
from typing import Dict, Any


class DataProcessor:
    """
    Data processor class that handles INACBG-based pricing adjustments.
    
    Processing logic:
    - For each row, check the 4th digit of INACBG value
    - If digit 4 is '0': multiply TARIF_RS, PENUNJANG, RADIOLOGI, LABORATORIUM by 0.79 (79%)
    - If digit 4 is 'I', 'II', or 'III': multiply TARIF_RS, PENUNJANG, RADIOLOGI, LABORATORIUM by 0.73 (73%)
    """
    
    def __init__(self):
        self.raw_data = None
        self.processed_data = None
    
    def load_raw_data(self, dataframe: pd.DataFrame) -> bool:
        """
        Load raw data from dataframe
        
        Args:
            dataframe: Raw data from uploaded file
            
        Returns:
            bool: True if successful
        """
        self.raw_data = dataframe.copy()
        return True
    
    def process_data(self) -> pd.DataFrame:
        """
        Process raw data based on INACBG 4th digit logic
        
        Returns:
            pd.DataFrame: Processed data with adjusted pricing
        """
        if self.raw_data is None:
            raise ValueError("No raw data loaded. Please load data first.")
        
        # Create a copy of raw data for processing
        self.processed_data = self.raw_data.copy()
        
        # Define columns to be adjusted based on INACBG
        pricing_columns = ['TARIF_RS', 'PENUNJANG', 'RADIOLOGI', 'LABORATORIUM']
        
        # Ensure all pricing columns exist and are numeric
        for col in pricing_columns:
            if col in self.processed_data.columns:
                self.processed_data[col] = pd.to_numeric(self.processed_data[col], errors='coerce').fillna(0)
            else:
                # If column doesn't exist, create it with 0 values
                self.processed_data[col] = 0
        
        # Process each row based on INACBG 4th digit
        for index, row in self.processed_data.iterrows():
            inacbg_value = str(row.get('INACBG', ''))
            
            # For INACBG format like "K-4-17-I", we need to find the last part after the last dash
            # which represents the severity level (0, I, II, III)
            if '-' in inacbg_value:
                parts = inacbg_value.split('-')
                if len(parts) >= 4:
                    severity_level = parts[-1]  # Last part after the last dash
                    
                    # Apply pricing adjustments based on severity level
                    if severity_level == '0':
                        # Multiply by 0.79 (79%)
                        multiplier = 0.79
                    elif severity_level.upper() in ['I', 'II', 'III']:
                        # Multiply by 0.73 (73%)
                        multiplier = 0.73
                    else:
                        # No adjustment for other values
                        multiplier = 1.0
                else:
                    multiplier = 1.0
            else:
                multiplier = 1.0
            
            # Apply multiplier to pricing columns
            for col in pricing_columns:
                if col in self.processed_data.columns:
                    original_value = self.processed_data.at[index, col]
                    adjusted_value = original_value * multiplier
                    self.processed_data.at[index, col] = round(adjusted_value, 2)
        
        return self.processed_data
    
    def get_processed_data(self) -> pd.DataFrame:
        """
        Get the processed data
        
        Returns:
            pd.DataFrame: Processed data with INACBG-based pricing adjustments
        """
        if self.processed_data is None:
            raise ValueError("No processed data available. Please process data first.")
        
        return self.processed_data
    
    def get_raw_data(self) -> pd.DataFrame:
        """
        Get the raw data
        
        Returns:
            pd.DataFrame: Raw data before processing
        """
        if self.raw_data is None:
            raise ValueError("No raw data available.")
        
        return self.raw_data
    
    def has_data(self) -> bool:
        """
        Check if data is available
        
        Returns:
            bool: True if data is available, False otherwise
        """
        return self.raw_data is not None
    
    def has_processed_data(self) -> bool:
        """
        Check if processed data is available
        
        Returns:
            bool: True if processed data is available, False otherwise
        """
        return self.processed_data is not None
    
    def get_processing_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the processing applied
        
        Returns:
            dict: Summary of processing statistics
        """
        if self.processed_data is None:
            return {"error": "No processed data available"}
        
        summary = {
            "total_rows": len(self.processed_data),
            "inacbg_0_count": 0,
            "inacbg_i_ii_iii_count": 0,
            "inacbg_other_count": 0,
            "pricing_adjustments_applied": 0
        }
        
        for index, row in self.processed_data.iterrows():
            inacbg_value = str(row.get('INACBG', ''))
            
            # Parse INACBG format like "K-4-17-I"
            if '-' in inacbg_value:
                parts = inacbg_value.split('-')
                if len(parts) >= 4:
                    severity_level = parts[-1]  # Last part after the last dash
                    
                    if severity_level == '0':
                        summary["inacbg_0_count"] += 1
                        summary["pricing_adjustments_applied"] += 1
                    elif severity_level.upper() in ['I', 'II', 'III']:
                        summary["inacbg_i_ii_iii_count"] += 1
                        summary["pricing_adjustments_applied"] += 1
                    else:
                        summary["inacbg_other_count"] += 1
                else:
                    summary["inacbg_other_count"] += 1
            else:
                summary["inacbg_other_count"] += 1
        
        return summary
