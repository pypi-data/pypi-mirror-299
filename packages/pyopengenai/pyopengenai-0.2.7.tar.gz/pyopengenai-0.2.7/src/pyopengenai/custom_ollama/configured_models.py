from ._custom_ollama import CustomChatOllama
class Qwen27InstructChatOllama(CustomChatOllama):
    model: str = "qwen2.5:7b-instruct"
    base_url: str = "http://192.168.170.76:8888"
    temperature: float = 0.0
    num_predict:int =8000

class Qwen21Point5BInstructChatOllama(CustomChatOllama):
    model: str = "qwen2.5:1.5b-instruct"
    base_url: str = "http://192.168.170.76:8888"
    temperature: float = 0.0
    num_predict:int =8000

class GPU27B(CustomChatOllama):
    model: str = "qwen2.5:7b-instruct"
    base_url: str = "http://192.168.162.49:8888"
    temperature: float = 0.0
    num_predict:int =8000

class GPU215B(CustomChatOllama):
    model: str = "qwen2.5:1.5   b-instruct"
    base_url: str = "http://192.168.162.49:8888"
    temperature: float = 0.0
    num_predict:int =8000

