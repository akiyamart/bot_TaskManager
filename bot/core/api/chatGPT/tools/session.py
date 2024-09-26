import aiohttp
from typing import List, Dict, Any

from ....settings import Config

class OpenAISession:
    def __init__(self, api_key: str, proxy_username: str, proxy_pass: str, proxy_endpoint: str):
        self.api_key = api_key
        self.proxy = f"http://{proxy_username}:{proxy_pass}@{proxy_endpoint}"
    
    async def _post_request(self, url: str, json_data: Dict[str, Any]) -> Dict[str, Any]:
        async with aiohttp.ClientSession(headers={
                    "Content-Type": "application/json", 
                    "Authorization": f"Bearer {self.api_key}"
                }) as session: 
            async with session.post(url, json=json_data, proxy=self.proxy) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_message = await response.text()
                    raise Exception(f"Ошибка API: {response.status} - {error_message}")

    def _add_pre_prompt(self, messages: List[Dict[str, Any]], system_prompt: str) -> List[Dict[str, Any]]:
        pre_prompt = {"role": "system", "content": system_prompt}
        return [pre_prompt] + messages

    async def chat_gpt_session_text(self, messages: List[Dict[str, Any]], system_prompt: str = "Ты ассистент, который помогает с задачами и расписанием.") -> Dict[str, Any]:
        url = "https://api.openai.com/v1/chat/completions"
        full_messages = self._add_pre_prompt(messages, system_prompt)
        json_data = {
            "model": "gpt-4o",
            "messages": full_messages
        }
        return await self._post_request(url, json_data)

    async def chat_gpt_session_voice(self, voice_data: bytes) -> Dict[str, Any]: 
        url = "https://api.openai.com/v1/audio/transcriptions"
        json_data = {
            "model": "whisper-1",
            "file": voice_data
        }
        return await self._post_request(url, json_data)

chat_gpt_session = OpenAISession(
    api_key=Config.OPENAI_API_KEY,
    proxy_username=Config.PROXY_USERNAME,
    proxy_pass=Config.PROXY_PASS,
    proxy_endpoint=Config.PROXY_ENDPOINT
)

