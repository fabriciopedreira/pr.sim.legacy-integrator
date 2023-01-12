import traceback
from dataclasses import dataclass, field
from typing import Any, Optional

import httpx
import jwt
from httpx import ConnectTimeout, HTTPError, HTTPStatusError
from jwt import DecodeError
from loguru import logger

from app.domain.common.exception_base import AuthenticationException, UnauthorizedException
from app.internal.config import BASIC_HEADERS, KEYCLOAK_BASE_URL, KEYCLOAK_REALM
from app.internal.config.settings import AUTH_CACHE_EXPIRATION, AUTH_CACHE_MAXSIZE
from app.internal.utils import cache, exc_info


@dataclass
class Auth:
    oidc_uri: str = field(init=False)

    def __post_init__(self):
        self.oidc_uri = f"{KEYCLOAK_BASE_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect"

    async def token_validation(self, token: str) -> bool:
        """Validate token for authentication
        :param: token: Str token

        :return: bool: True for valid token
        """
        certs = await self.__get_certs()
        kid = self.get_kid(token)
        result = list(filter(lambda key: (key["kid"] == kid), certs))  # type: ignore

        return bool(result)

    @staticmethod
    def get_kid(token: str) -> Optional[Any]:
        """Get Kit value for JWT token header
        :param: token: Str token

        :return: str: kit value
        """
        try:
            token_header = jwt.get_unverified_header(token)
            return token_header.get("kid")
        except DecodeError as exc:
            raise UnauthorizedException(stacktrace=traceback.format_exception_only(*exc_info())) from exc

    @cache(seconds=AUTH_CACHE_EXPIRATION, maxsize=AUTH_CACHE_MAXSIZE)
    async def __get_certs(self) -> Optional[Any]:
        """Get keycloak certs for token validation
        :return: dict[str, Any]"""
        url = self.oidc_uri + "/certs"

        result = await self.__make_request(url, headers=BASIC_HEADERS)

        return result.get("keys")

    @classmethod
    async def __make_request(cls, url: str, headers: dict[str, Any]) -> dict[str, Any]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)

            if response.status_code != 200:
                response.raise_for_status()

            logger.info(f"[+] Request for [{url}] - [StatusCode={response.status_code}]")

            return response.json()
        except (HTTPStatusError, ConnectTimeout, HTTPError) as exc:
            raise AuthenticationException(stacktrace=traceback.format_exception_only(*exc_info())) from exc

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))
