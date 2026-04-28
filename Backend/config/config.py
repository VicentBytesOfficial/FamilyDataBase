from dotenv import load_dotenv
import os


def initConfig(role: str, userInput: str|None = None, passwordInput: str|None = None) -> list[str]:
    load_dotenv()
    """Loads config depends on role"""
    if role == "server" or role == "developer":
        host = str(os.getenv('HOST'))
        port = int(os.getenv('PORT'))    
        return [host, port]
    elif role == "client":
        # TODO
        pass