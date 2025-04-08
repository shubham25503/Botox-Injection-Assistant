from datetime import datetime
from bson import ObjectId


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