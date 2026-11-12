from pydantic import BaseModel


class Configuration(BaseModel):
    """
    Class containing all the configuration options and variables used by the package
    """
    host: str = "localhost"
    port: int = 1865
    auth_key: str | None = None
    secure_connection: bool = False
    # Max size (bytes) of a single WebSocket message; None disables the limit
    ws_max_size: int | None = 256 * 1024 * 1024
