import hashlib
from datetime import datetime, timedelta

def generate_short_url(original_url: str) -> str:
    return hashlib.md5(original_url.encode()).hexdigest()[:6]

def calculate_expiry(hours: int = 24) -> datetime:
    return datetime.utcnow() + timedelta(hours=hours)

def is_expired(expiry_time: datetime) -> bool:
    return datetime.utcnow() > expiry_time
