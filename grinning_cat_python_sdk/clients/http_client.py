from requests.structures import CaseInsensitiveDict
from requests_toolbelt.sessions import BaseUrlSession
from urllib.parse import urlunparse


class HttpClient:
    def __init__(
        self,
        host: str,
        port: int | None = None,
        apikey: str | None = None,
        is_https: bool = False
    ):
        self.host = host
        self.port = port
        self.apikey = apikey
        self.token = None
        self.agent_id = None
        self.user_id = None
        self.chat_id = None
        self.is_https = is_https

    def set_token(self, token: str):
        self.token = token
        return self

    def get_http_uri(self) -> str:
        scheme = "https" if self.is_https else "http"
        netloc = f"{self.host}:{self.port}" if self.port else self.host

        return urlunparse((scheme, netloc, "", "", "", ""))

    def _base_headers(self) -> dict[str, str]:
        headers: dict[str, str] = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        elif self.apikey:
            headers["Authorization"] = f"Bearer {self.apikey}"
        return headers

    def get_client(
        self,
        agent_id: str | None = None,
        user_id: str | None = None,
        chat_id: str | None = None,
    ) -> BaseUrlSession:
        if not self.apikey and not self.token:
            raise ValueError("You must provide an apikey or a token")

        self.agent_id = agent_id
        self.user_id = user_id
        self.chat_id = chat_id

        headers = self._base_headers()
        if agent_id:
            headers["X-Agent-ID"] = agent_id
        if user_id:
            headers["X-User-ID"] = user_id
        if chat_id:
            headers["X-Chat-ID"] = chat_id

        session = BaseUrlSession(base_url=self.get_http_uri())
        session.headers = CaseInsensitiveDict(headers)
        return session

    def get_base_session(self) -> BaseUrlSession:
        session = BaseUrlSession(base_url=self.get_http_uri())
        session.headers = CaseInsensitiveDict(self._base_headers())

        return session
