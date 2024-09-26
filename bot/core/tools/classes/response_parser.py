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

    def get_task_data(self, user_id: int):
        if not self.parsed_data:
            return None

        return {
            'user_id': user_id,
            'title': self.parsed_data.get('title'),
            'description': self.parsed_data.get('description'),
            'due_date': self.parsed_data.get('due_date'),
            'end_time': self.parsed_data.get('end_time'),
            'intersection' : self.parsed_data.get('intersection'),
        }

    def get_emoji(self):
        return self.parsed_data.get('emoji', "")
