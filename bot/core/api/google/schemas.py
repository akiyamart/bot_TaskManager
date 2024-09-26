from pydantic import BaseModel
from typing import Union, Optional

from pydantic import BaseModel

class Event(BaseModel):
    id: Optional[str] = None 
    timezone: Optional[str] = "Europe/Moscow"
    summary: str
    description: str
    location: str
    start: str
    end: str

    @classmethod
    def from_google_calendar_event(cls, event_data):
        return cls(
            id=event_data['id'],
            summary=event_data.get('summary', ''),
            description=event_data.get('description', ''),
            location=event_data.get('location', ''),
            start=event_data['start'].get('dateTime', event_data['start'].get('date')),
            end=event_data['end'].get('dateTime', event_data['end'].get('date')),
            timezone=event_data['start'].get('timeZone', '')
        )
