"""
Monitoring and observability for NeuroSmriti
Integrates logging, metrics, and error tracking
"""
import logging
import time
from functools import wraps
from typing import Callable
import sys

from loguru import logger

# Remove default loguru handler
logger.remove()

# Add custom formatters
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO",
    colorize=True
)

logger.add(
    "logs/app.log",
    rotation="1 day",
    retention="30 days",
    compression="zip",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="INFO"
)

logger.add(
    "logs/errors.log",
    rotation="1 day",
    retention="90 days",
    compression="zip",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="ERROR"
)


def log_execution_time(func: Callable) -> Callable:
    """Decorator to log function execution time"""

    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            elapsed = time.time() - start_time
            logger.info(f"{func.__name__} completed in {elapsed:.3f}s")
            return result
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(f"{func.__name__} failed after {elapsed:.3f}s: {e}")
            raise

    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time
            logger.info(f"{func.__name__} completed in {elapsed:.3f}s")
            return result
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(f"{func.__name__} failed after {elapsed:.3f}s: {e}")
            raise

    import asyncio
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper


class PerformanceMonitor:
    """Track performance metrics"""

    def __init__(self):
        self.metrics = {
            "api_calls": 0,
            "ml_predictions": 0,
            "errors": 0,
            "total_response_time": 0.0,
            "predictions_response_time": 0.0
        }

    def record_api_call(self, endpoint: str, duration: float, status_code: int):
        """Record API call metrics"""
        self.metrics["api_calls"] += 1
        self.metrics["total_response_time"] += duration

        if status_code >= 400:
            self.metrics["errors"] += 1

        logger.info(f"API: {endpoint} | {status_code} | {duration:.3f}s")

    def record_prediction(self, model: str, duration: float):
        """Record ML prediction metrics"""
        self.metrics["ml_predictions"] += 1
        self.metrics["predictions_response_time"] += duration
        logger.info(f"Prediction: {model} | {duration:.3f}s")

    def get_stats(self) -> dict:
        """Get current metrics"""
        avg_response_time = (
            self.metrics["total_response_time"] / self.metrics["api_calls"]
            if self.metrics["api_calls"] > 0 else 0
        )

        avg_prediction_time = (
            self.metrics["predictions_response_time"] / self.metrics["ml_predictions"]
            if self.metrics["ml_predictions"] > 0 else 0
        )

        return {
            **self.metrics,
            "avg_response_time": avg_response_time,
            "avg_prediction_time": avg_prediction_time,
            "error_rate": (
                self.metrics["errors"] / self.metrics["api_calls"]
                if self.metrics["api_calls"] > 0 else 0
            )
        }


# Global performance monitor instance
performance_monitor = PerformanceMonitor()


def setup_sentry(dsn: str = None):
    """Initialize Sentry for error tracking (if configured)"""
    if not dsn:
        logger.info("Sentry DSN not configured - skipping error tracking setup")
        return

    try:
        import sentry_sdk
        from sentry_sdk.integrations.fastapi import FastApiIntegration
        from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

        sentry_sdk.init(
            dsn=dsn,
            traces_sample_rate=0.1,  # 10% of transactions
            profiles_sample_rate=0.1,  # 10% of profiling
            integrations=[
                FastApiIntegration(),
                SqlalchemyIntegration()
            ],
            environment="production",
            before_send=lambda event, hint: event if event.get("level") != "info" else None
        )

        logger.info("Sentry error tracking initialized")

    except ImportError:
        logger.warning("Sentry SDK not installed - skipping error tracking")
    except Exception as e:
        logger.error(f"Failed to initialize Sentry: {e}")
