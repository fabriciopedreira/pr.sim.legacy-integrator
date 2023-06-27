import asyncio
import json

import httpx
from fastapi import status
from loguru import logger

from app.domain.common.exception_base import (
    APIError,
    ServiceBadRequestException,
    ServiceNotFoundException,
    ServiceRequestException,
    ServiceUnauthorizedException,
    UnprocessEntity,
)
from app.internal.config.settings import BASIC_HEADERS, MAX_ATTEMPTS, REQUEST_TIMEOUT, TIME_SLEEP, VERIFY


class RequestApi:
    def __init__(self, url, headers=None, token=None):
        self.url = url
        if headers is None:
            self.headers = BASIC_HEADERS
        else:
            self.headers = headers
        if token:
            self.headers["Authorization"] = f"Bearer {token}"

    async def post_with_retry(self, payload, verify=VERIFY, timeout=REQUEST_TIMEOUT, dumps=True, path=""):
        for attempt in range(MAX_ATTEMPTS):
            logger.info(f"[+] Sending request to {self.url + path}, attempt #{attempt + 1}")
            response = await self.post(payload, attempt, verify, timeout, dumps, path)

            if response:
                return response

            logger.warning(f"[*] Request failed. Waiting {TIME_SLEEP}s before new attempt.")
            await asyncio.sleep(TIME_SLEEP)
        raise APIError(detail="The request could not be made, 'MAX_ATTEMPTS' not configured.")

    async def post(self, payload, attempt, verify, timeout, dumps, path=""):
        try:
            async with httpx.AsyncClient(verify=verify) as client:
                payload = json.dumps(payload) if dumps else payload
                response = await client.post(url=self.url + path, data=payload, headers=self.headers, timeout=timeout)

            if 500 <= response.status_code <= 599:
                response.raise_for_status()

            logger.info(f"[*] Request for [{self.url + path}] - [StatusCode={response.status_code}]")
            return self.process_response(response)
        except (httpx.HTTPError, httpx.TimeoutException, AttributeError, TypeError) as exc:
            logger.opt(exception=True).error(f"[-] Exception - [URL={self.url}] - [ERROR={self.__get_error(exc)}]")
            if attempt == MAX_ATTEMPTS - 1:
                raise APIError(f"[URL={self.url + path}] - [ERROR={self.__get_error(exc)}]") from exc
            return False

    async def get_with_retry(self, params=None, verify=VERIFY, timeout=REQUEST_TIMEOUT, dumps=True):
        for attempt in range(MAX_ATTEMPTS):
            logger.info(f"[+] Sending request to {self.url}, attempt #{attempt + 1}")
            response = await self.get(params, attempt, verify, timeout, dumps)
            if response:
                return response

            logger.warning(f"[*] Request failed. Waiting {TIME_SLEEP}s before new attempt.")
            await asyncio.sleep(TIME_SLEEP)
        raise APIError(detail="The request could not be made, 'MAX_ATTEMPTS' not configured.")

    async def get(self, params, attempt, verify, timeout, dumps):
        try:
            async with httpx.AsyncClient(verify=verify) as client:
                params = json.dumps(params) if dumps else params
                response = await client.get(url=self.url, params=params, headers=self.headers, timeout=timeout)

            if 500 <= response.status_code <= 599:
                response.raise_for_status()

            logger.info(f"[*] Request for [{self.url}] - [StatusCode={response.status_code}]")
            return self.process_response(response)
        except (httpx.HTTPError, httpx.TimeoutException, AttributeError, TypeError) as exc:
            logger.opt(exception=True).error(f"[-] Exception - [URL={self.url}] - [ERROR={self.__get_error(exc)}]")
            if attempt == MAX_ATTEMPTS - 1:
                raise APIError(detail=f"[URL={self.url}] - [ERROR={self.__get_error(exc)}]") from exc
            return False

    def process_response(self, response):
        if response.status_code == status.HTTP_200_OK:
            return response.json()
        if response.status_code == status.HTTP_201_CREATED:
            return response.content
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            raise ServiceBadRequestException(stacktrace=[response.text])
        if response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
            raise UnprocessEntity(stacktrace=[], detail=response.text)
        if response.status_code == status.HTTP_404_NOT_FOUND:
            raise ServiceNotFoundException(stacktrace=[response.text])
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            raise ServiceUnauthorizedException(stacktrace=[response.text])
        raise ServiceRequestException([])

    @staticmethod
    def __get_error(exc):
        try:
            return exc.response.text
        except AttributeError:
            return str(exc)
