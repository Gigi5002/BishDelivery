# fastapi-core/src/domain/models.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class UserDomain:
    id: Optional[int]
    email: str
    hashed_password: str
    full_name: str
    phone: str
    role: str  # client, courier, restaurant_admin, super_admin
    is_active: bool
    created_at: datetime