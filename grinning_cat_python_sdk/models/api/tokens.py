from pydantic import BaseModel


class TokenOutput(BaseModel):
    access_token: str
    token_type: str | None = "bearer"
    expires_in: int | None = None
    refresh_token: str | None = None
    refresh_expires_in: int | None = None


class User(BaseModel):
    id: str
    username: str
    permissions: dict[str, list[str]]
    created_at: float | None = None
    updated_at: float | None = None


class AgentMatch(BaseModel):
    agent_name: str
    user: User


class MeOutput(BaseModel):
    success : bool
    agents: list[AgentMatch]
    auto_selected: bool
