from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Trip:
    
    trip_id: int
    date_time_utc: datetime
    tap_type: str
    stop_id: str
    company_id: str
    bus_id: str
    pan: int
