from typing import Any

from grinning_cat_python_sdk.endpoints.base import AbstractEndpoint
from grinning_cat_python_sdk.models.api.tokens import TokenOutput, MeOutput
from grinning_cat_python_sdk.utils import deserialize


class AuthEndpoint(AbstractEndpoint):
    def __init__(self, client: "GrinningCatClient"):
        super().__init__(client)
        self.prefix = "/auth"

    def token(self, username: str, password: str) -> TokenOutput:
        """
        This endpoint is used to get a token for the user. The token is used to authenticate the user in the system. When
        the token expires, the user must request a new token.
        """
        response = self.get_http_session().post(
            self.format_url("/token"),
            json={
                "username": username,
                "password": password,
            },
        )
        response.raise_for_status()

        result = deserialize(response.json(), TokenOutput)
        self.client.add_token(result.access_token)

        return result

    def refresh(self, refresh_token: str) -> TokenOutput:
        """
        Exchanges a refresh token for a new access token. The refresh token is rotated: the one returned here
        replaces it and must be used for the next refresh, since the submitted one is consumed and reusing it
        revokes the whole session.
        """
        response = self.get_http_session().post(
            self.format_url("/refresh"),
            json={"refresh_token": refresh_token},
        )
        response.raise_for_status()

        result = deserialize(response.json(), TokenOutput)
        self.client.add_token(result.access_token)

        return result

    def logout(self, refresh_token: str) -> None:
        """
        Revokes the session the refresh token belongs to. Already-issued access tokens stay valid until they expire.
        """
        response = self.get_http_session().post(
            self.format_url("/logout"),
            json={"refresh_token": refresh_token},
        )
        response.raise_for_status()

    def get_available_permissions(self) -> dict[int | str, Any]:
        """
        This endpoint is used to get a list of available permissions in the system. The permissions are used to define
        the access rights of the users in the system. The permissions are defined by the system administrator.
        :return array<int|string, Any>, the available permissions
        """
        response = self.get_http_client().get(self.format_url("/available-permissions"))
        response.raise_for_status()

        return response.json()

    def me(self, token: str) -> MeOutput:
        """
        This endpoint is used to get the current user information. The user information includes the list of agents
        the user has access to. This endpoint requires authentication.
        """
        self.client.add_token(token)

        response = self.get_http_client().get("/me")
        response.raise_for_status()

        result = deserialize(response.json(), MeOutput)
        return result
