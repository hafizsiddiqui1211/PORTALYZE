"""HTTP client utility for Resume Analyzer Core"""
import asyncio
import httpx
import time
from typing import Optional, Dict, Any
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
from src.utils.logger import get_logger
from src.utils.constants import (
    HTTP_TIMEOUT_DEFAULT,
    HTTP_MAX_RETRIES,
    HTTP_RETRY_BASE_DELAY,
    HTTP_RETRY_MAX_DELAY
)


class HTTPClient:
    """Async HTTP client with retry logic and timeout handling"""

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
        self.logger = get_logger("HTTPClient")

        # Create async client with default timeout
        self.client = httpx.AsyncClient(timeout=httpx.Timeout(timeout))

    def close(self):
        """Close the HTTP client"""
        if self.client:
            try:
                self.client.close()
            except Exception as e:
                self.logger.error(f"Error closing HTTP client: {str(e)}")

    @retry(
        stop=stop_after_attempt(HTTP_MAX_RETRIES),
        wait=wait_exponential(multiplier=HTTP_RETRY_BASE_DELAY, min=1, max=HTTP_RETRY_MAX_DELAY),
        retry=retry_if_exception_type((httpx.RequestError, httpx.TimeoutException)),
        reraise=True
    )
    async def get(self, url: str, headers: Optional[Dict[str, str]] = None) -> Optional[httpx.Response]:
        """
        Perform GET request with retry logic.

        Args:
            url: The URL to make the request to
            headers: Optional headers to include in the request

        Returns:
            httpx.Response if successful, None if failed after retries
        """
        try:
            self.logger.debug(f"Making GET request to {url}")

            response = await self.client.get(url, headers=headers)

            # Log response status
            self.logger.debug(f"GET request to {url} returned status {response.status_code}")

            # Raise an exception for bad status codes so retry logic can handle them
            response.raise_for_status()

            return response
        except httpx.HTTPStatusError as e:
            self.logger.warning(f"HTTP error {e.response.status_code} for {url}, retrying...")
            raise  # Re-raise to trigger retry
        except httpx.RequestError as e:
            self.logger.warning(f"Request error for {url}: {str(e)}, retrying...")
            raise  # Re-raise to trigger retry
        except Exception as e:
            self.logger.error(f"Unexpected error during GET request to {url}: {str(e)}")
            raise  # Re-raise to trigger retry

    @retry(
        stop=stop_after_attempt(HTTP_MAX_RETRIES),
        wait=wait_exponential(multiplier=HTTP_RETRY_BASE_DELAY, min=1, max=HTTP_RETRY_MAX_DELAY),
        retry=retry_if_exception_type((httpx.RequestError, httpx.TimeoutException)),
        reraise=True
    )
    async def post(self, url: str, data: Optional[Dict[str, Any]] = None, json_data: Optional[Any] = None,
                   headers: Optional[Dict[str, str]] = None) -> Optional[httpx.Response]:
        """
        Perform POST request with retry logic.

        Args:
            url: The URL to make the request to
            data: Optional form data to send
            json_data: Optional JSON data to send
            headers: Optional headers to include in the request

        Returns:
            httpx.Response if successful, None if failed after retries
        """
        try:
            self.logger.debug(f"Making POST request to {url}")

            response = await self.client.post(url, data=data, json=json_data, headers=headers)

            # Log response status
            self.logger.debug(f"POST request to {url} returned status {response.status_code}")

            # Raise an exception for bad status codes so retry logic can handle them
            response.raise_for_status()

            return response
        except httpx.HTTPStatusError as e:
            self.logger.warning(f"HTTP error {e.response.status_code} for {url}, retrying...")
            raise  # Re-raise to trigger retry
        except httpx.RequestError as e:
            self.logger.warning(f"Request error for {url}: {str(e)}, retrying...")
            raise  # Re-raise to trigger retry
        except Exception as e:
            self.logger.error(f"Unexpected error during POST request to {url}: {str(e)}")
            raise  # Re-raise to trigger retry

    async def check_url_accessibility(self, url: str, headers: Optional[Dict[str, str]] = None) -> bool:
        """
        Check if a URL is accessible without downloading the full content.

        Args:
            url: The URL to check
            headers: Optional headers to include in the request

        Returns:
            True if accessible, False otherwise
        """
        try:
            response = await self.get(url, headers)
            return response is not None and response.status_code < 400
        except Exception as e:
            self.logger.warning(f"URL {url} is not accessible: {str(e)}")
            return False

    async def get_content_length(self, url: str, headers: Optional[Dict[str, str]] = None) -> Optional[int]:
        """
        Get the content length of a URL without downloading the full content.

        Args:
            url: The URL to check
            headers: Optional headers to include in the request

        Returns:
            Content length in bytes, or None if not available
        """
        try:
            response = await self.client.head(url, headers=headers)
            response.raise_for_status()
            content_length = response.headers.get("content-length")
            return int(content_length) if content_length else None
        except Exception as e:
            self.logger.warning(f"Could not get content length for {url}: {str(e)}")
            return None


# Synchronous wrapper functions for easier use in non-async contexts
def sync_get(url: str, headers: Optional[Dict[str, str]] = None, timeout: int = HTTP_TIMEOUT_DEFAULT) -> Optional[httpx.Response]:
    """
    Synchronous wrapper for GET request.

    Args:
        url: The URL to make the request to
        headers: Optional headers to include in the request
        timeout: Request timeout in seconds

    Returns:
        httpx.Response if successful, None if failed
    """
    async def _async_get():
        client = HTTPClient(timeout=timeout)
        try:
            return await client.get(url, headers)
        finally:
            client.close()

    return asyncio.run(_async_get())


def sync_post(url: str, data: Optional[Dict[str, Any]] = None, json_data: Optional[Any] = None,
              headers: Optional[Dict[str, str]] = None, timeout: int = HTTP_TIMEOUT_DEFAULT) -> Optional[httpx.Response]:
    """
    Synchronous wrapper for POST request.

    Args:
        url: The URL to make the request to
        data: Optional form data to send
        json_data: Optional JSON data to send
        headers: Optional headers to include in the request
        timeout: Request timeout in seconds

    Returns:
        httpx.Response if successful, None if failed
    """
    async def _async_post():
        client = HTTPClient(timeout=timeout)
        try:
            return await client.post(url, data, json_data, headers)
        finally:
            client.close()

    return asyncio.run(_async_post())


def sync_check_url_accessibility(url: str, headers: Optional[Dict[str, str]] = None,
                                 timeout: int = HTTP_TIMEOUT_DEFAULT) -> bool:
    """
    Synchronous wrapper to check URL accessibility.

    Args:
        url: The URL to check
        headers: Optional headers to include in the request
        timeout: Request timeout in seconds

    Returns:
        True if accessible, False otherwise
    """
    async def _async_check():
        client = HTTPClient(timeout=timeout)
        try:
            return await client.check_url_accessibility(url, headers)
        finally:
            client.close()

    return asyncio.run(_async_check())