from typing import Mapping
from google.oauth2.service_account import Credentials
import googleapiclient.discovery

from .schemas import Event

class GoogleCalendarAsync:
    def __init__(self, credentials: Mapping[str, str]) -> None:
        self.credentials = Credentials.from_service_account_info(credentials)
        self.calendar_service = googleapiclient.discovery.build('calendar', 'v3', credentials=self.credentials, cache_discovery=False)

    async def add_event(self, event: Event, calendar_id: str = "primary",) -> Event:
        event_body = await self.event_to_dict(event)
        event = await self.calendar_service.events().insert(calendarId=calendar_id, body=event_body).execute()
        return Event.from_google_calendar_event(event)

    async def update_event(self, event: Event, calendar_id: str = "primary",) -> Event:
        event_body = await self.event_to_dict(event)
        event = await self.calendar_service.events().update(calendarId=calendar_id, eventId=event.id, body=event_body).execute()
        return Event.from_google_calendar_event(event)

    async def delete_event(self, event: Event, calendar_id: str = "primary",) -> bool:
        try:
            await self.calendar_service.events().delete(calendarId=calendar_id, eventId=event.id).execute()
            return True
        except Exception as err:
            print(err)
            return False

    async def get_event_as_dict(self, event: Event, calendar_id: str = "primary",):
        event = await self.calendar_service.events().get(calendarId=calendar_id, eventId=event.id).execute()
        return Event.from_google_calendar_event(event)

    @staticmethod
    def event_to_dict(event: Event):
        return {
            'summary': event.summary,
            'start': {
                "dataTime": event.start,
                "timeZone": event.timezone
            },
            'end': {
                "dataTime": event.end,
                "timeZone": event.timezone
            },
            'description': event.description,
            'location': event.location
        }