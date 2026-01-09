"""Rate limiter service for Resume Analyzer Core"""
import time
import asyncio
import random
from typing import Callable, Any, Optional, Dict
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    AsyncRetrying,
    RetryError
)
from src.utils.logger import get_logger
from src.utils.constants import (
    RATE_LIMIT_BASE_DELAY,
    RATE_LIMIT_MAX_DELAY,
    RATE_LIMIT_MAX_RETRIES
)


class RateLimiter:
    """Handles rate limiting with exponential backoff using tenacity"""

    def __init__(
        self,
        base_delay: float = RATE_LIMIT_BASE_DELAY,
        max_delay: float = RATE_LIMIT_MAX_DELAY,
        max_retries: int = RATE_LIMIT_MAX_RETRIES
    ):
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.max_retries = max_retries
        self.logger = get_logger("RateLimiter")

    def create_retry_decorator(self, exception_types: tuple = (Exception,)):
        """
        Create a retry decorator with exponential backoff.

        Args:
            exception_types: Tuple of exception types to retry on

        Returns:
            Retry decorator
        """
        return retry(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_exponential(
                multiplier=self.base_delay,
                min=self.base_delay,
                max=self.max_delay
            ),
            retry=retry_if_exception_type(exception_types),
            reraise=True
        )

    async def execute_with_backoff_async(
        self,
        func: Callable,
        *args,
        exception_types: tuple = (Exception,),
        **kwargs
    ) -> Any:
        """
        Execute an async function with exponential backoff retry logic.

        Args:
            func: The async function to execute
            *args: Arguments to pass to the function
            exception_types: Tuple of exception types to retry on
            **kwargs: Keyword arguments to pass to the function

        Returns:
            Result of the function call
        """
        retry_decorator = self.create_retry_decorator(exception_types)

        @retry_decorator
        async def _execute_with_retry():
            start_time = time.time()
            self.logger.debug(f"Executing function {func.__name__} with args {args}")

            try:
                result = await func(*args, **kwargs)
                end_time = time.time()
                self.logger.debug(f"Function {func.__name__} completed successfully in {end_time - start_time:.2f}s")
                return result
            except exception_types as e:
                end_time = time.time()
                self.logger.warning(
                    f"Function {func.__name__} failed after {end_time - start_time:.2f}s: {str(e)}. "
                    f"Attempt {self.max_retries - _execute_with_retry.retry.statistics['attempt_number'] + 1}/{self.max_retries}"
                )
                raise

        return await _execute_with_retry()

    def execute_with_backoff_sync(
        self,
        func: Callable,
        *args,
        exception_types: tuple = (Exception,),
        **kwargs
    ) -> Any:
        """
        Execute a sync function with exponential backoff retry logic.

        Args:
            func: The sync function to execute
            *args: Arguments to pass to the function
            exception_types: Tuple of exception types to retry on
            **kwargs: Keyword arguments to pass to the function

        Returns:
            Result of the function call
        """
        retry_decorator = self.create_retry_decorator(exception_types)

        @retry_decorator
        def _execute_with_retry():
            start_time = time.time()
            self.logger.debug(f"Executing function {func.__name__} with args {args}")

            try:
                result = func(*args, **kwargs)
                end_time = time.time()
                self.logger.debug(f"Function {func.__name__} completed successfully in {end_time - start_time:.2f}s")
                return result
            except exception_types as e:
                end_time = time.time()
                self.logger.warning(
                    f"Function {func.__name__} failed after {end_time - start_time:.2f}s: {str(e)}. "
                    f"Attempt {self.max_retries - _execute_with_retry.retry.statistics['attempt_number'] + 1}/{self.max_retries}"
                )
                raise

        return _execute_with_retry()

    async def wait_with_jitter(self, delay: float) -> None:
        """
        Wait for a specified delay with random jitter.

        Args:
            delay: Base delay in seconds
        """
        # Add jitter to prevent thundering herd
        jitter = random.uniform(0, delay * 0.1)  # Up to 10% additional random delay
        total_delay = delay + jitter

        self.logger.debug(f"Waiting {total_delay:.2f}s with jitter (base: {delay}s, jitter: {jitter:.2f}s)")
        await asyncio.sleep(total_delay)

    def track_usage(self, resource_name: str, limit: int, window_seconds: int = 3600) -> Dict[str, Any]:
        """
        Track resource usage for rate limiting purposes.

        Args:
            resource_name: Name of the resource being tracked
            limit: Request limit for the window
            window_seconds: Time window in seconds

        Returns:
            Dictionary with usage statistics
        """
        # This would typically involve storing usage in a database or cache
        # For now, we'll just return a mock implementation
        return {
            "resource": resource_name,
            "limit": limit,
            "window_seconds": window_seconds,
            "used": 0,  # Would be retrieved from storage
            "remaining": limit,  # Would be calculated from storage
            "reset_time": time.time() + window_seconds  # Would be calculated from storage
        }

    async def acquire_slot_async(
        self,
        resource_name: str,
        limit: int,
        window_seconds: int = 3600,
        wait_for_slot: bool = True
    ) -> bool:
        """
        Attempt to acquire a slot for a rate-limited resource.

        Args:
            resource_name: Name of the resource
            limit: Request limit for the window
            window_seconds: Time window in seconds
            wait_for_slot: Whether to wait if no slots are available

        Returns:
            True if slot acquired, False if not
        """
        usage_stats = self.track_usage(resource_name, limit, window_seconds)

        if usage_stats["remaining"] > 0:
            # Would actually reserve the slot in storage
            self.logger.debug(f"Acquired slot for {resource_name}, {usage_stats['remaining']-1} remaining")
            return True
        elif wait_for_slot:
            # Calculate time until reset and wait
            time_until_reset = usage_stats["reset_time"] - time.time()
            if time_until_reset > 0:
                self.logger.debug(f"No slots available for {resource_name}, waiting {time_until_reset:.2f}s for reset")
                await asyncio.sleep(time_until_reset)
                return True
        else:
            self.logger.warning(f"No slots available for {resource_name}")
            return False

    def acquire_slot_sync(
        self,
        resource_name: str,
        limit: int,
        window_seconds: int = 3600,
        wait_for_slot: bool = True
    ) -> bool:
        """
        Synchronously attempt to acquire a slot for a rate-limited resource.

        Args:
            resource_name: Name of the resource
            limit: Request limit for the window
            window_seconds: Time window in seconds
            wait_for_slot: Whether to wait if no slots are available

        Returns:
            True if slot acquired, False if not
        """
        usage_stats = self.track_usage(resource_name, limit, window_seconds)

        if usage_stats["remaining"] > 0:
            # Would actually reserve the slot in storage
            self.logger.debug(f"Acquired slot for {resource_name}, {usage_stats['remaining']-1} remaining")
            return True
        elif wait_for_slot:
            # Calculate time until reset and wait
            time_until_reset = usage_stats["reset_time"] - time.time()
            if time_until_reset > 0:
                self.logger.debug(f"No slots available for {resource_name}, waiting {time_until_reset:.2f}s for reset")
                time.sleep(time_until_reset)
                return True
        else:
            self.logger.warning(f"No slots available for {resource_name}")
            return False

    def create_rate_limited_function(
        self,
        func: Callable,
        resource_name: str,
        limit: int,
        window_seconds: int = 3600,
        exception_types: tuple = (Exception,)
    ) -> Callable:
        """
        Create a rate-limited version of a function with retry logic.

        Args:
            func: The function to wrap
            resource_name: Name of the resource being rate-limited
            limit: Request limit for the window
            window_seconds: Time window in seconds
            exception_types: Tuple of exception types to retry on

        Returns:
            Rate-limited function with retry logic
        """
        if asyncio.iscoroutinefunction(func):
            async def rate_limited_wrapper(*args, **kwargs):
                # Acquire a slot first
                acquired = await self.acquire_slot_async(resource_name, limit, window_seconds)
                if not acquired:
                    raise Exception(f"Rate limit exceeded for {resource_name}")

                # Execute with backoff
                return await self.execute_with_backoff_async(
                    func, *args, exception_types=exception_types, **kwargs
                )
            return rate_limited_wrapper
        else:
            def rate_limited_wrapper(*args, **kwargs):
                # Acquire a slot first
                acquired = self.acquire_slot_sync(resource_name, limit, window_seconds)
                if not acquired:
                    raise Exception(f"Rate limit exceeded for {resource_name}")

                # Execute with backoff
                return self.execute_with_backoff_sync(
                    func, *args, exception_types=exception_types, **kwargs
                )
            return rate_limited_wrapper

    def wait_if_needed(self) -> None:
        """
        Simple wait method to implement rate limiting with a basic delay.
        This is a basic implementation that waits for a fixed delay to respect rate limits.
        """
        # Using a small random delay to prevent synchronized requests
        delay = random.uniform(0.5, 1.5)  # Random delay between 0.5 and 1.5 seconds
        self.logger.debug(f"Applying rate limiting delay of {delay:.2f}s")
        time.sleep(delay)


class AsyncRateLimiter:
    """Async version of RateLimiter using AsyncRetrying"""

    def __init__(
        self,
        base_delay: float = RATE_LIMIT_BASE_DELAY,
        max_delay: float = RATE_LIMIT_MAX_DELAY,
        max_retries: int = RATE_LIMIT_MAX_RETRIES
    ):
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.max_retries = max_retries
        self.logger = get_logger("AsyncRateLimiter")

    async def execute_with_backoff(
        self,
        func: Callable,
        *args,
        exception_types: tuple = (Exception,),
        **kwargs
    ) -> Any:
        """
        Execute an async function with exponential backoff retry logic using AsyncRetrying.

        Args:
            func: The async function to execute
            *args: Arguments to pass to the function
            exception_types: Tuple of exception types to retry on
            **kwargs: Keyword arguments to pass to the function

        Returns:
            Result of the function call
        """
        retrying = AsyncRetrying(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_exponential(
                multiplier=self.base_delay,
                min=self.base_delay,
                max=self.max_delay
            ),
            retry=retry_if_exception_type(exception_types),
            reraise=True
        )

        async def _execute_with_retry():
            start_time = time.time()
            self.logger.debug(f"Executing function {func.__name__} with args {args}")

            try:
                result = await func(*args, **kwargs)
                end_time = time.time()
                self.logger.debug(f"Function {func.__name__} completed successfully in {end_time - start_time:.2f}s")
                return result
            except exception_types as e:
                end_time = time.time()
                attempt_number = retrying.statistics["attempt_number"] if "attempt_number" in retrying.statistics else 1
                self.logger.warning(
                    f"Function {func.__name__} failed after {end_time - start_time:.2f}s: {str(e)}. "
                    f"Attempt {attempt_number}/{self.max_retries}"
                )
                raise

        async for attempt in retrying:
            with attempt:
                return await _execute_with_retry()


# Global rate limiter instance
default_rate_limiter = RateLimiter()