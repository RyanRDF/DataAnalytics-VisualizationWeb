"""
Base handler class for all data handlers
"""
import pandas as pd
from typing import List, Optional, Tuple, Dict, Any
from abc import ABC, abstractmethod

from utils.validators import validate_required_columns, validate_date_range, validate_sort_parameters
from utils.data_processing import apply_date_filter, apply_sorting, apply_specific_filter
from core.database_query_service import DatabaseQueryService


class BaseHandler(ABC):
    """
    Base class for all data handlers
    Provides common functionality for data processing, filtering, and validation
    """
    
    def __init__(self, data_handler):
        self.data_handler = data_handler
        self.required_columns = self._get_required_columns()
        self.view_name = self._get_view_name()
        self.db_query_service = DatabaseQueryService()
    
    @abstractmethod
    def _get_required_columns(self) -> List[str]:
        """Get list of required columns for this handler"""
        pass
    
    @abstractmethod
    def _get_view_name(self) -> str:
        """Get the view name for this handler"""
        pass
    
    @abstractmethod
    def _query_database(self, filters: Dict[str, Any]) -> pd.DataFrame:
        """Query data from database with filters"""
        pass
    
    @abstractmethod
    def _process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process the data with specific business logic"""
        pass
    
    def process_data(self, sort_column: Optional[str] = None, sort_order: str = 'ASC', 
                    start_date: Optional[str] = None, end_date: Optional[str] = None,
                    filter_column: Optional[str] = None, filter_value: Optional[str] = None) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        """
        Process data with flexible filtering and sorting logic
        Supports any combination of filters
        
        Args:
            sort_column: Column name to sort by
            sort_order: Sort order ('ASC' or 'DESC')
            start_date: Start date for filtering
            end_date: End date for filtering
            filter_column: Column name to filter by
            filter_value: Value to filter for
            
        Returns:
            Tuple of (processed_dataframe, error_message)
        """
        try:
            # Prepare filters for database query
            filters = {}
            if start_date:
                filters['start_date'] = start_date
            if end_date:
                filters['end_date'] = end_date
            
            # Get data from database (with date filters if any)
            df = self._query_database(filters)
            
            if df.empty:
                return None, f"No {self.view_name} data available in database. Please import data first."
            
            # Apply specific processing logic
            df = self._process_data(df)
            
            # Apply column-specific filter if provided
            if filter_column and filter_value and filter_column in df.columns:
                df = apply_specific_filter(df, filter_column, filter_value)
            
            # Apply sorting if provided
            if sort_column and sort_column in df.columns:
                ascending = sort_order.upper() == 'ASC'
                df = df.sort_values(by=sort_column, ascending=ascending)
            
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
        # Process data with all filters including specific filter
        df, error = self.process_data(sort_column, sort_order, start_date, end_date, filter_column, filter_value)
        if error:
            return None, error
        
        return df, None
    
    def get_table(self, sort_column: Optional[str] = None, sort_order: str = 'ASC',
                  start_date: Optional[str] = None, end_date: Optional[str] = None,
                  filter_column: Optional[str] = None, filter_value: Optional[str] = None) -> Tuple[str, Optional[str]]:
        """
        Get HTML table representation of processed data with flexible filtering
        Supports any combination of filters
        
        Args:
            sort_column: Column name to sort by
            sort_order: Sort order ('ASC' or 'DESC')
            start_date: Start date for filtering
            end_date: End date for filtering
            filter_column: Column name to filter by
            filter_value: Value to filter for
            
        Returns:
            Tuple of (html_table, error_message)
        """
        df, error = self.process_data(sort_column, sort_order, start_date, end_date, filter_column, filter_value)
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
        This method now uses the unified get_table method for consistency
        
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
        # Use the unified get_table method which now supports all filter combinations
        return self.get_table(sort_column, sort_order, start_date, end_date, filter_column, filter_value)
    
    def get_columns(self) -> List[str]:
        """
        Get available columns for this handler
        
        Returns:
            List of column names
        """
        try:
            # Get sample data from database and process it to get final columns
            sample_df = self._query_database({})
            if sample_df.empty:
                return self.required_columns
            
            # Process the data to get the final column structure (after removing duplicates)
            processed_df = self._process_data(sample_df)
            return list(processed_df.columns)
        except Exception as e:
            print(f"Error getting columns: {e}")
            return self.required_columns
