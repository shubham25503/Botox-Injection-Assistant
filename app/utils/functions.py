from datetime import datetime
from bson import ObjectId
from datetime import datetime
from typing import Any, Dict
from fastapi import HTTPException

def create_response(
    status_code: int, 
    success: bool, 
    message: str, 
    result: Any = None
) -> Dict[str, Any]:
    """
    Utility function to create a standardized response format.
    
    Args:
        status_code: HTTP status code (200 for success, etc.)
        success: Whether the operation was successful (True or False)
        message: A message describing the status of the response
        result: The actual data being returned (can be an object or an array)
    
    Returns:
        A dictionary in the desired response format.
    """
    response = {
        "status": status_code,
        "success": success,
        "message": message,
        "result": result if isinstance(result, dict) else {"data": result} if isinstance(result, list) else None,  
        "timestamp": datetime.now().isoformat() 
    }
    return response

def handle_exception(exception: Exception, message: str, error_code:int=400):
    return create_response(error_code, False, message, str(exception))



def convert_objectid_and_datetime(doc):
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            doc[key] = str(value)
        elif isinstance(value, datetime):
            doc[key] = value.isoformat()
        elif isinstance(value, list):
            doc[key] = [convert_objectid_and_datetime(item) if isinstance(item, dict) else item for item in value]
        elif isinstance(value, dict):
            doc[key] = convert_objectid_and_datetime(value)
    return doc

def objectid_to_str(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not serializable")
