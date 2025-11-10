"""
Centralized handler registry to avoid duplication
"""
from typing import Dict, Optional, Any
from core.base_handler import BaseHandler


class HandlerRegistry:
    """Central registry for all data handlers"""
    
    # Handler name mappings - single source of truth
    HANDLER_MAP = {
        'keuangan': 'financial',
        'financial': 'financial',
        'pasien': 'patient',
        'patient': 'patient',
        'selisih-tarif': 'selisih_tarif',
        'selisih_tarif': 'selisih_tarif',
        'los': 'los',
        'inacbg': 'inacbg',
        'ventilator': 'ventilator'
    }
    
    # Route view names mapping
    VIEW_NAMES = {
        'financial': 'keuangan',
        'patient': 'pasien',
        'selisih_tarif': 'selisih-tarif',
        'los': 'los',
        'inacbg': 'inacbg',
        'ventilator': 'ventilator'
    }
    
    @staticmethod
    def normalize_handler_name(handler_name: str) -> str:
        """
        Normalize handler name to canonical form
        
        Args:
            handler_name: Handler name (can be alias or canonical)
            
        Returns:
            Canonical handler name
        """
        return HandlerRegistry.HANDLER_MAP.get(handler_name, handler_name)
    
    @staticmethod
    def get_view_name(handler_name: str) -> str:
        """
        Get route view name for handler
        
        Args:
            handler_name: Handler name
            
        Returns:
            View name for routes
        """
        canonical = HandlerRegistry.normalize_handler_name(handler_name)
        return HandlerRegistry.VIEW_NAMES.get(canonical, canonical)
    
    @staticmethod
    def get_handler(data_handler, handler_name: str) -> Optional[BaseHandler]:
        """
        Get handler instance by name from data_handler
        
        Args:
            data_handler: DataHandler instance
            handler_name: Handler name (can be alias or canonical)
            
        Returns:
            Handler instance or None if not found
        """
        canonical_name = HandlerRegistry.normalize_handler_name(handler_name)
        
        handler_attr_map = {
            'financial': 'financial_handler',
            'patient': 'patient_handler',
            'selisih_tarif': 'selisih_tarif_handler',
            'los': 'los_handler',
            'inacbg': 'inacbg_handler',
            'ventilator': 'ventilator_handler'
        }
        
        attr_name = handler_attr_map.get(canonical_name)
        if attr_name and hasattr(data_handler, attr_name):
            return getattr(data_handler, attr_name)
        
        return None




