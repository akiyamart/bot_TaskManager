import json
import re

class AIResponseParser:
    def __init__(self, raw_response: str):
        self.raw_response = raw_response
        self.parsed_data = None

    def parse(self):
        json_match = re.search(r'```json\n(.*?)\n```', self.raw_response, re.DOTALL)

        if json_match:
            json_data = json_match.group(1)
            json_data = re.sub(r'//.*?\n', '', json_data)
            json_data = re.sub(r'/\*.*?\*/', '', json_data, flags=re.DOTALL)
            self.parsed_data = json.loads(json_data)
        else:
            return None

    def get_event_data(self, user_id: int):
        if not self.parsed_data:
            return None
        
        code = self.parsed_data.get('code')

        if code == "1":
            return {
                'code': code, 
                'user_id': user_id,
                'title': self.parsed_data.get('title'),
                'description': self.parsed_data.get('description'),
                'due_date': self.parsed_data.get('due_date'),
                'start_time': self.parsed_data.get('start_time'),
                'end_time': self.parsed_data.get('end_time'),
                'reminder': self.parsed_data.get('reminder'),
                'overlap_warning': self.parsed_data.get('overlap_warning', "")
            }

        elif code == "2":
            return {
                'code': code, 
                'UUID': self.parsed_data.get('UUID'),
                'user_id': user_id,
                'title': self.parsed_data.get('title'),
                'description': self.parsed_data.get('description'),
                'due_date': self.parsed_data.get('due_date'),
                'start_time': self.parsed_data.get('start_time'),
                'end_time': self.parsed_data.get('end_time'),
                'reminder': self.parsed_data.get('reminder'),
                'overlap_warning': self.parsed_data.get('overlap_warning', "")
            }

        elif code == "3":
            return {
                'code': code, 
                'user_id': user_id,
                'events': self.parsed_data.get('events', [])
            }

        elif code == "4":
            return {
                'code': code, 
                'UUID': self.parsed_data.get('UUID'),
                'title': self.parsed_data.get('title'),
                'description': self.parsed_data.get('description'),
                'due_date': self.parsed_data.get('due_date'),
                'start_time': self.parsed_data.get('start_time'),
            }

        elif code == "5":
            return {
                'code': code, 
                'error': self.parsed_data.get('error')
            }

        return None

    def get_emoji(self):
        return self.parsed_data.get('emoji', "")
