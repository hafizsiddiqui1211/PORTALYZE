"""HTTP Client Service for Resume Analyzer Core"""
import httpx
import asyncio
from typing import Optional, Dict, Any
from src.utils.logger import get_logger
from src.utils.constants import (
    HTTP_TIMEOUT_DEFAULT,
    HTTP_MAX_RETRIES,
    HTTP_RETRY_BASE_DELAY,
    HTTP_RETRY_MAX_DELAY
)
from tenacity import retry, stop_after_attempt, wait_exponential


class HttpClient:
    """HTTP client with retry logic and timeout handling for profile extraction"""

    def __init__(
        self,
        timeout: int = HTTP_TIMEOUT_DEFAULT,
        max_retries: int = HTTP_MAX_RETRIES,
        base_delay: float = HTTP_RETRY_BASE_DELAY,
        max_delay: float = HTTP_RETRY_MAX_DELAY
    ):
        self.timeout = timeout
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.logger = get_logger("HttpClient")

        # Create async client with default timeout
        self.async_client = httpx.AsyncClient(timeout=timeout)

    @retry(
        stop=stop_after_attempt(HTTP_MAX_RETRIES),
        wait=wait_exponential(multiplier=HTTP_RETRY_BASE_DELAY, min=1, max=HTTP_RETRY_MAX_DELAY)
    )
    async def get(self, url: str, headers: Optional[Dict[str, str]] = None) -> httpx.Response:
        """
        Perform an HTTP GET request with retry logic.

        Args:
            url: URL to request
            headers: Optional headers to include in the request

        Returns:
            httpx.Response object

        Raises:
            httpx.RequestError: If the request fails after all retries
        """
        self.logger.debug(f"Making GET request to: {url}")

        try:
            response = await self.async_client.get(url, headers=headers or {})
            self.logger.debug(f"GET request to {url} returned status: {response.status_code}")

            # Raise an exception for bad status codes so tenacity can retry
            response.raise_for_status()

            return response
        except httpx.RequestError as e:
            self.logger.warning(f"Request failed for {url}: {str(e)}")
            # Re-raise to trigger retry
            raise

    @retry(
        stop=stop_after_attempt(HTTP_MAX_RETRIES),
        wait=wait_exponential(multiplier=HTTP_RETRY_BASE_DELAY, min=1, max=HTTP_RETRY_MAX_DELAY)
    )
    async def post(self, url: str, data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> httpx.Response:
        """
        Perform an HTTP POST request with retry logic.

        Args:
            url: URL to request
            data: Optional data to send in the request body
            headers: Optional headers to include in the request

        Returns:
            httpx.Response object

        Raises:
            httpx.RequestError: If the request fails after all retries
        """
        self.logger.debug(f"Making POST request to: {url}")

        try:
            response = await self.async_client.post(url, json=data, headers=headers or {})
            self.logger.debug(f"POST request to {url} returned status: {response.status_code}")

            # Raise an exception for bad status codes so tenacity can retry
            response.raise_for_status()

            return response
        except httpx.RequestError as e:
            self.logger.warning(f"Request failed for {url}: {str(e)}")
            # Re-raise to trigger retry
            raise

    async def close(self):
        """Close the HTTP client and release resources."""
        await self.async_client.aclose()

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()


# Synchronous wrapper for use in non-async contexts
class SyncHttpClient:
    """Synchronous wrapper for HttpClient to be used in non-async contexts."""

    def __init__(
        self,
        timeout: int = HTTP_TIMEOUT_DEFAULT,
        max_retries: int = HTTP_MAX_RETRIES,
        base_delay: float = HTTP_RETRY_BASE_DELAY,
        max_delay: float = HTTP_RETRY_MAX_DELAY
    ):
        self.timeout = timeout
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.logger = get_logger("SyncHttpClient")

    def get(self, url: str, headers: Optional[Dict[str, str]] = None) -> httpx.Response:
        """
        Perform a synchronous HTTP GET request.

        Args:
            url: URL to request
            headers: Optional headers to include in the request

        Returns:
            httpx.Response object
        """
        # Run the async client in a new event loop
        return asyncio.run(self._async_get(url, headers))

    async def _async_get(self, url: str, headers: Optional[Dict[str, str]] = None) -> httpx.Response:
        """Internal async method to perform GET request."""
        async with HttpClient(
            timeout=self.timeout,
            max_retries=self.max_retries,
            base_delay=self.base_delay,
            max_delay=self.max_delay
        ) as client:
            return await client.get(url, headers)

    def post(self, url: str, data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> httpx.Response:
        """
        Perform a synchronous HTTP POST request.

        Args:
            url: URL to request
            data: Optional data to send in the request body
            headers: Optional headers to include in the request

        Returns:
            httpx.Response object
        """
        # Run the async client in a new event loop
        return asyncio.run(self._async_post(url, data, headers))

    async def _async_post(self, url: str, data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> httpx.Response:
        """Internal async method to perform POST request."""
        async with HttpClient(
            timeout=self.timeout,
            max_retries=self.max_retries,
            base_delay=self.base_delay,
            max_delay=self.max_delay
        ) as client:
            return await client.post(url, data, headers)