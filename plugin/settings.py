from flogin import Settings

class DeepSeekSettings(Settings):
    model: str
    api_key: str
    prompt_stop: str
    default_prompt: str
    api_endpoint: str