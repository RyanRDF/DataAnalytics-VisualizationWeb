"""
Base handler class for all data handlers
"""
import pandas as pd
from typing import List, Optional, Tuple, Dict, Any
from abc import ABC, abstractmethod

from ..utils.validators import validate_required_columns, validate_date_range, validate_sort_parameters
from ..utils.data_processing import apply_date_filter, apply_sorting, apply_specific_filter


class BaseHandler(ABC):
    """
    Base class for all data handlers
    Provides common functionality for data processing, filtering, and validation
    """
    
    def __init__(self, data_handler):
        self.data_handler = data_handler
        self.required_columns = self._get_required_columns()
        self.view_name = self._get_view_name()
    
    @abstractmethod
    def _get_required_columns(self) -> List[str]:
        """Get list of required columns for this handler"""
        pass
    
    @abstractmethod
    def _get_view_name(self) -> str:
        """Get the view name for this handler"""
        pass
    
    @abstractmethod
    def _process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process the data with specific business logic"""
        pass
    
    def process_data(self, sort_column: Optional[str] = None, sort_order: str = 'ASC', 
                    start_date: Optional[str] = None, end_date: Optional[str] = None) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        """
        Process data with common filtering and sorting logic
        
        Args:
            sort_column: Column name to sort by
            sort_order: Sort order ('ASC' or 'DESC')
            start_date: Start date for filtering
            end_date: End date for filtering
            
        Returns:
            Tuple of (processed_dataframe, error_message)
        """
        # Validate data availability
        if self.data_handler.current_df is None:
            return None, "No data available. Please upload a file first."
        
        # Validate required columns
        is_valid, error = validate_required_columns(self.data_handler.current_df, self.required_columns)
        if not is_valid:
            return None, error
        
        # Validate date range
        is_valid, error = validate_date_range(start_date, end_date)
        if not is_valid:
            return None, error
        
        # Validate sort column
        available_columns = list(self.data_handler.current_df.columns)
        is_valid, error = validate_sort_parameters(sort_column, available_columns)
        if not is_valid:
            return None, error
        
        try:
            # Create a copy with required columns
            df = self.data_handler.current_df[self.required_columns].copy()
            
            # Apply specific processing logic
            df = self._process_data(df)
            
            # Apply date filtering
            df = apply_date_filter(df, start_date, end_date)
            
            # Apply sorting
            df = apply_sorting(df, sort_column, sort_order)
            
            return df, None
            
        except Exception as e:
            return None, f"Error processing {self.view_name} data: {str(e)}"
    
    def process_data_with_specific_filter(self, filter_column: str, filter_value: str, 
                                        sort_column: Optional[str] = None, sort_order: str = 'ASC',
                                        start_date: Optional[str] = None, end_date: Optional[str] = None) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        """
        Process data with specific column filter
        
        Args:
            filter_column: Column name to filter by
            filter_value: Value to filter for
            sort_column: Column name to sort by
            sort_order: Sort order ('ASC' or 'DESC')
            start_date: Start date for filtering
            end_date: End date for filtering
            
        Returns:
            Tuple of (processed_dataframe, error_message)
        """
        # First process data normally
        df, error = self.process_data(sort_column, sort_order, start_date, end_date)
        if error:
            return None, error
        
        # Apply specific filter
        df = apply_specific_filter(df, filter_column, filter_value)
        
        return df, None
    
    def get_table(self, sort_column: Optional[str] = None, sort_order: str = 'ASC',
                  start_date: Optional[str] = None, end_date: Optional[str] = None) -> Tuple[str, Optional[str]]:
        """
        Get HTML table representation of processed data
        
        Args:
            sort_column: Column name to sort by
            sort_order: Sort order ('ASC' or 'DESC')
            start_date: Start date for filtering
            end_date: End date for filtering
            
        Returns:
            Tuple of (html_table, error_message)
        """
        df, error = self.process_data(sort_column, sort_order, start_date, end_date)
        if error:
            return "", error
        
        try:
            table_html = df.to_html(classes='data-table', index=False, escape=False)
            return table_html, None
        except Exception as e:
            return "", f"Error generating {self.view_name} table: {str(e)}"
    
    def get_table_with_specific_filter(self, filter_column: str, filter_value: str,
                                     sort_column: Optional[str] = None, sort_order: str = 'ASC',
                                     start_date: Optional[str] = None, end_date: Optional[str] = None) -> Tuple[str, Optional[str]]:
        """
        Get HTML table with specific column filter
        
        Args:
            filter_column: Column name to filter by
            filter_value: Value to filter for
            sort_column: Column name to sort by
            sort_order: Sort order ('ASC' or 'DESC')
            start_date: Start date for filtering
            end_date: End date for filtering
            
        Returns:
            Tuple of (html_table, error_message)
        """
        df, error = self.process_data_with_specific_filter(filter_column, filter_value, sort_column, sort_order, start_date, end_date)
        if error:
            return "", error
        
        try:
            table_html = df.to_html(classes='data-table', index=False, escape=False)
            return table_html, None
        except Exception as e:
            return "", f"Error generating {self.view_name} table: {str(e)}"
    
    def get_columns(self) -> List[str]:
        """
        Get available columns for this handler
        
        Returns:
            List of column names
        """
        if self.data_handler.current_df is None:
            return []
        
        # Return columns that exist in the current data
        return [col for col in self.required_columns if col in self.data_handler.current_df.columns]
