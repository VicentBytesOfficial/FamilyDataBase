from Backend.server import main as serverStart

def backend(config: list[str]) -> list[str] | None:
    """Starts backend function"""
    serverStart(config)