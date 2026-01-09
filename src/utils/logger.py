"""Logging utilities for Resume Analyzer Core"""
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> logging.Logger:
    """
    Set up logging configuration for the application.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path to write logs to

    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger("ResumeAnalyzer")
    logger.setLevel(getattr(logging, log_level.upper()))

    # Prevent adding multiple handlers if logger already configured
    if logger.handlers:
        return logger

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Create file handler if log_file is specified
    if log_file:
        # Ensure directory exists
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, log_level.upper()))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Also log to a daily rotating file in logs directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # Create a filename with today's date
    today = datetime.now().strftime("%Y%m%d")
    daily_log_file = logs_dir / f"resume_analyzer_{today}.log"

    daily_handler = logging.FileHandler(daily_log_file)
    daily_handler.setLevel(getattr(logging, log_level.upper()))
    daily_handler.setFormatter(formatter)
    logger.addHandler(daily_handler)

    return logger


def get_logger(name: str = "ResumeAnalyzer") -> logging.Logger:
    """
    Get a logger instance.

    Args:
        name: Name of the logger (default: "ResumeAnalyzer")

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


def log_function_call(logger: logging.Logger, level: str = "INFO"):
    """
    Decorator to log function calls.

    Args:
        logger: Logger instance to use
        level: Logging level for the log message
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger.log(getattr(logging, level.upper()), f"Calling function: {func.__name__}")
            try:
                result = func(*args, **kwargs)
                logger.log(getattr(logging, level.upper()), f"Function {func.__name__} completed successfully")
                return result
            except Exception as e:
                logger.error(f"Function {func.__name__} failed with error: {str(e)}")
                raise
        return wrapper
    return decorator


# Pre-configured logger instance
app_logger = setup_logging(
    log_level=os.getenv("LOG_LEVEL", "INFO"),
    log_file=os.getenv("LOG_FILE", "logs/resume_analyzer.log")
)


def log_analysis_start(logger: logging.Logger, resume_id: str, filename: str):
    """
    Log the start of a resume analysis.

    Args:
        logger: Logger instance
        resume_id: Unique identifier for the resume
        filename: Original filename of the resume
    """
    logger.info(f"Starting analysis for resume ID: {resume_id}, filename: {filename}")


def log_analysis_complete(logger: logging.Logger, resume_id: str, ats_score: float):
    """
    Log the completion of a resume analysis.

    Args:
        logger: Logger instance
        resume_id: Unique identifier for the resume
        ats_score: Calculated ATS score
    """
    logger.info(f"Analysis completed for resume ID: {resume_id}, ATS score: {ats_score}")


def log_file_upload(logger: logging.Logger, filename: str, file_size: int, session_id: str):
    """
    Log file upload event.

    Args:
        logger: Logger instance
        filename: Name of the uploaded file
        file_size: Size of the file in bytes
        session_id: Session ID associated with the upload
    """
    logger.info(f"File uploaded: {filename}, size: {file_size} bytes, session: {session_id}")


def log_file_processing_error(logger: logging.Logger, filename: str, error: str):
    """
    Log file processing error.

    Args:
        logger: Logger instance
        filename: Name of the file that failed processing
        error: Error message
    """
    logger.error(f"File processing failed for {filename}: {error}")


def log_keyword_suggestions(logger: logging.Logger, count: int, resume_id: str):
    """
    Log keyword suggestion generation.

    Args:
        logger: Logger instance
        count: Number of keyword suggestions generated
        resume_id: Resume ID associated with the suggestions
    """
    logger.info(f"Generated {count} keyword suggestions for resume ID: {resume_id}")


def log_pdf_generation(logger: logging.Logger, pdf_path: str, resume_id: str):
    """
    Log PDF report generation.

    Args:
        logger: Logger instance
        pdf_path: Path to the generated PDF
        resume_id: Resume ID associated with the report
    """
    logger.info(f"PDF report generated at {pdf_path} for resume ID: {resume_id}")


def log_performance(logger: logging.Logger, operation: str, duration: float, resume_id: str = None):
    """
    Log performance metrics for operations.

    Args:
        logger: Logger instance
        operation: Name of the operation
        duration: Duration of the operation in seconds
        resume_id: Optional resume ID associated with the operation
    """
    resume_info = f", resume ID: {resume_id}" if resume_id else ""
    logger.info(f"Operation '{operation}' completed in {duration:.2f}s{resume_info}")


def log_security_event(logger: logging.Logger, event_type: str, details: str, session_id: str = None):
    """
    Log security-related events.

    Args:
        logger: Logger instance
        event_type: Type of security event
        details: Details about the event
        session_id: Optional session ID
    """
    session_info = f", session: {session_id}" if session_id else ""
    logger.warning(f"Security event: {event_type}, details: {details}{session_info}")