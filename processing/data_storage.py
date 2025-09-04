import os
import json
import pickle
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class DataStorage:
    """
    Manages storage and retrieval of processed datasets with metadata
    """
    
    def __init__(self, storage_dir: str = "saved_data"):
        self.storage_dir = storage_dir
        self.metadata_file = os.path.join(storage_dir, "metadata.json")
        self.current_dataset_id = None
        
        # Ensure storage directory exists
        os.makedirs(storage_dir, exist_ok=True)
        
        # Load existing metadata
        self.metadata = self._load_metadata()
    
    def _load_metadata(self) -> Dict:
        """Load metadata from file"""
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}
    
    def _save_metadata(self):
        """Save metadata to file"""
        try:
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving metadata: {e}")
    
    def _generate_dataset_id(self, filename: str) -> str:
        """Generate unique dataset ID based on filename and timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.splitext(filename)[0]
        return f"{base_name}_{timestamp}"
    
    def save_dataset(self, filename: str, processed_data: pd.DataFrame, 
                    processing_summary: Dict) -> str:
        """
        Save a processed dataset with metadata
        
        Args:
            filename: Original filename
            processed_data: Processed DataFrame
            processing_summary: Processing statistics
            
        Returns:
            str: Dataset ID
        """
        dataset_id = self._generate_dataset_id(filename)
        
        # Save the processed data
        data_file = os.path.join(self.storage_dir, f"{dataset_id}.pkl")
        try:
            with open(data_file, 'wb') as f:
                pickle.dump(processed_data, f)
        except Exception as e:
            raise Exception(f"Error saving dataset: {e}")
        
        # Create metadata entry
        metadata_entry = {
            "dataset_id": dataset_id,
            "original_filename": filename,
            "saved_at": datetime.now().isoformat(),
            "display_name": filename,
            "data_file": data_file,
            "processing_summary": processing_summary,
            "row_count": len(processed_data),
            "column_count": len(processed_data.columns)
        }
        
        # Add to metadata
        self.metadata[dataset_id] = metadata_entry
        self._save_metadata()
        
        # Set as current dataset
        self.current_dataset_id = dataset_id
        
        return dataset_id
    
    def get_saved_datasets(self) -> List[Dict]:
        """
        Get list of all saved datasets with metadata
        
        Returns:
            List of dataset metadata dictionaries
        """
        datasets = []
        for dataset_id, metadata in self.metadata.items():
            # Check if data file still exists
            if os.path.exists(metadata.get("data_file", "")):
                datasets.append({
                    "dataset_id": dataset_id,
                    "display_name": metadata["display_name"],
                    "saved_at": metadata["saved_at"],
                    "row_count": metadata.get("row_count", 0),
                    "column_count": metadata.get("column_count", 0),
                    "processing_summary": metadata.get("processing_summary", {})
                })
            else:
                # Remove from metadata if file doesn't exist
                self._remove_dataset(dataset_id)
        
        # Sort by saved_at (newest first)
        datasets.sort(key=lambda x: x["saved_at"], reverse=True)
        return datasets
    
    def load_dataset(self, dataset_id: str) -> Tuple[pd.DataFrame, Dict]:
        """
        Load a saved dataset
        
        Args:
            dataset_id: ID of the dataset to load
            
        Returns:
            Tuple of (processed_data, processing_summary)
        """
        if dataset_id not in self.metadata:
            raise ValueError(f"Dataset {dataset_id} not found")
        
        metadata = self.metadata[dataset_id]
        data_file = metadata["data_file"]
        
        if not os.path.exists(data_file):
            raise ValueError(f"Data file for {dataset_id} not found")
        
        try:
            with open(data_file, 'rb') as f:
                processed_data = pickle.load(f)
            
            processing_summary = metadata.get("processing_summary", {})
            self.current_dataset_id = dataset_id
            
            return processed_data, processing_summary
        except Exception as e:
            raise Exception(f"Error loading dataset: {e}")
    
    def get_current_dataset_id(self) -> Optional[str]:
        """Get current dataset ID"""
        return self.current_dataset_id
    
    def _remove_dataset(self, dataset_id: str):
        """Remove dataset from metadata (internal use)"""
        if dataset_id in self.metadata:
            del self.metadata[dataset_id]
            self._save_metadata()
    
    def delete_dataset(self, dataset_id: str) -> bool:
        """
        Delete a saved dataset
        
        Args:
            dataset_id: ID of the dataset to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        if dataset_id not in self.metadata:
            return False
        
        metadata = self.metadata[dataset_id]
        data_file = metadata["data_file"]
        
        try:
            # Remove data file
            if os.path.exists(data_file):
                os.remove(data_file)
            
            # Remove from metadata
            del self.metadata[dataset_id]
            self._save_metadata()
            
            # Clear current dataset if it was deleted
            if self.current_dataset_id == dataset_id:
                self.current_dataset_id = None
            
            return True
        except Exception as e:
            print(f"Error deleting dataset: {e}")
            return False
    
    def get_dataset_info(self, dataset_id: str) -> Optional[Dict]:
        """Get information about a specific dataset"""
        return self.metadata.get(dataset_id)
    
    def cleanup_old_datasets(self, max_age_days: int = 30):
        """
        Clean up datasets older than specified days
        
        Args:
            max_age_days: Maximum age in days
        """
        from datetime import datetime, timedelta
        
        cutoff_date = datetime.now() - timedelta(days=max_age_days)
        datasets_to_remove = []
        
        for dataset_id, metadata in self.metadata.items():
            try:
                saved_at = datetime.fromisoformat(metadata["saved_at"])
                if saved_at < cutoff_date:
                    datasets_to_remove.append(dataset_id)
            except Exception:
                # If we can't parse the date, consider it old
                datasets_to_remove.append(dataset_id)
        
        for dataset_id in datasets_to_remove:
            self.delete_dataset(dataset_id)
        
        return len(datasets_to_remove)
