import aiohttp

class DeepSeek:
    def __init__(
            self,
            api_key: str,
            model: str,
            system_prompt,
            endpoint: str,
            session: aiohttp.ClientSession | None = None
            ) -> None:
        self._session = session or aiohttp.ClientSession(
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
        )
        self.api_key = api_key
        self.model = model
        self.system_prompt = system_prompt
        self.endpoint = endpoint

    async def get_answer(self, question) -> str:
        """
        Get the answer from DeepSeek API.
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": question}
            ]
        temperature = 1.3
        payload = {
            "messages": messages,
            "model": self.model,
            "temperature": temperature
        }
        async with self._session.post(
            self.endpoint,
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            },
            json=payload,
            timeout=20
        ) as response:
            if response.status != 200:
                error_message = f"API请求失败: HTTP状态码 {response.status}, 响应数据: {await response.text()}"
                return f"抱歉，发生了错误: {error_message}"
            
            # 解析API响应数据为dict
            try:
                res = await response.json()
            except Exception as e:
                error_message = f"API响应数据解析失败: {e}"
                return f"抱歉，发生了错误: {error_message}"
            
            try:
                result = res["choices"][0]["message"].get("content", "")
            except (KeyError, IndexError) as e:
                error_message = f"响应数据格式错误: {e}"
                return f"抱歉，发生了错误: {error_message}"
            return result

            
            

        