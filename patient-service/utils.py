"""Utility functions for PII masking"""
import re

def mask_pii(field_type: str, value: str) -> str:
    """Mask PII in logs"""
    if not value:
        return None
    
    if field_type == "email":
        parts = value.split("@")
        if len(parts) == 2:
            return f"{parts[0][:2]}***@{parts[1]}"
        return value[:2] + "***"
    
    elif field_type == "phone":
        if len(value) >= 4:
            return value[:2] + "***" + value[-2:]
        return "***"
    
    elif field_type == "name":
        if len(value) > 2:
            return value[:2] + "***"
        return "***"
    
    return value

