"""
Tracing and observability setup utilities.

This module provides functions to enable and configure tracing for the Project Forge
multi-agent system using LangSmith or LangFuse.
"""

import os
import logging
from typing import Optional


logger = logging.getLogger(__name__)


def setup_langsmith_tracing() -> bool:
    """
    Set up LangSmith tracing if configured via environment variables.

    Checks for the following environment variables:
    - LANGCHAIN_TRACING_V2: Set to "true" to enable tracing
    - LANGCHAIN_API_KEY: Your LangSmith API key
    - LANGCHAIN_PROJECT: Project name (defaults to "project-forge")
    - LANGCHAIN_ENDPOINT: API endpoint (defaults to LangSmith cloud)

    Returns:
        True if LangSmith tracing is enabled and configured, False otherwise

    Usage:
        if setup_langsmith_tracing():
            logger.info("LangSmith tracing enabled")
    """
    tracing_enabled = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
    api_key = os.getenv("LANGCHAIN_API_KEY", "")

    if not tracing_enabled:
        logger.debug("LangSmith tracing not enabled (LANGCHAIN_TRACING_V2 not set to 'true')")
        return False

    if not api_key:
        logger.warning(
            "LANGCHAIN_TRACING_V2 is enabled but LANGCHAIN_API_KEY is not set. "
            "Tracing will not work without a valid API key."
        )
        return False

    project_name = os.getenv("LANGCHAIN_PROJECT", "project-forge")
    endpoint = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")

    logger.info(f"LangSmith tracing enabled for project: {project_name}")
    logger.debug(f"LangSmith endpoint: {endpoint}")

    return True


def setup_langfuse_tracing() -> bool:
    """
    Set up LangFuse tracing if configured via environment variables.

    Checks for the following environment variables:
    - LANGFUSE_PUBLIC_KEY: Your LangFuse public key
    - LANGFUSE_SECRET_KEY: Your LangFuse secret key
    - LANGFUSE_HOST: LangFuse host URL (defaults to cloud)

    Returns:
        True if LangFuse tracing is enabled and configured, False otherwise

    Note:
        LangFuse integration requires the langfuse package to be installed:
        pip install langfuse

    Usage:
        if setup_langfuse_tracing():
            logger.info("LangFuse tracing enabled")
    """
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY", "")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY", "")

    if not public_key or not secret_key:
        logger.debug("LangFuse tracing not configured (keys not set)")
        return False

    host = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")

    try:
        # Try to import langfuse to check if it's installed
        import langfuse  # noqa: F401
        logger.info(f"LangFuse tracing enabled (host: {host})")
        return True
    except ImportError:
        logger.warning(
            "LangFuse keys are configured but langfuse package is not installed. "
            "Install with: pip install langfuse"
        )
        return False


def setup_tracing(verbose: bool = False) -> dict:
    """
    Set up all available tracing backends.

    This is a convenience function that attempts to set up both LangSmith and
    LangFuse tracing based on environment variables.

    Args:
        verbose: Whether to log detailed setup information

    Returns:
        Dictionary with tracing status for each backend:
        {
            "langsmith": bool,
            "langfuse": bool,
            "any_enabled": bool
        }

    Usage:
        status = setup_tracing(verbose=True)
        if status["any_enabled"]:
            print("Tracing is enabled!")
    """
    if verbose:
        logger.setLevel(logging.DEBUG)

    langsmith = setup_langsmith_tracing()
    langfuse = setup_langfuse_tracing()

    status = {
        "langsmith": langsmith,
        "langfuse": langfuse,
        "any_enabled": langsmith or langfuse
    }

    if not status["any_enabled"]:
        logger.info(
            "No tracing backends configured. "
            "Set LANGCHAIN_TRACING_V2=true or configure LangFuse to enable tracing."
        )
    else:
        enabled_backends = []
        if langsmith:
            enabled_backends.append("LangSmith")
        if langfuse:
            enabled_backends.append("LangFuse")
        logger.info(f"Tracing enabled via: {', '.join(enabled_backends)}")

    return status


def get_tracing_info() -> dict:
    """
    Get information about current tracing configuration without enabling it.

    Returns:
        Dictionary with tracing configuration details:
        {
            "langsmith": {
                "enabled": bool,
                "has_api_key": bool,
                "project": str or None,
                "endpoint": str or None
            },
            "langfuse": {
                "enabled": bool,
                "has_keys": bool,
                "host": str or None,
                "package_installed": bool
            }
        }

    Usage:
        info = get_tracing_info()
        if info["langsmith"]["enabled"]:
            print(f"LangSmith project: {info['langsmith']['project']}")
    """
    langchain_enabled = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
    langchain_api_key = bool(os.getenv("LANGCHAIN_API_KEY", ""))

    langfuse_public_key = bool(os.getenv("LANGFUSE_PUBLIC_KEY", ""))
    langfuse_secret_key = bool(os.getenv("LANGFUSE_SECRET_KEY", ""))

    try:
        import langfuse  # noqa: F401
        langfuse_installed = True
    except ImportError:
        langfuse_installed = False

    return {
        "langsmith": {
            "enabled": langchain_enabled,
            "has_api_key": langchain_api_key,
            "project": os.getenv("LANGCHAIN_PROJECT", "project-forge") if langchain_enabled else None,
            "endpoint": os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com") if langchain_enabled else None
        },
        "langfuse": {
            "enabled": langfuse_public_key and langfuse_secret_key,
            "has_keys": langfuse_public_key and langfuse_secret_key,
            "host": os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com") if (langfuse_public_key and langfuse_secret_key) else None,
            "package_installed": langfuse_installed
        }
    }


# Auto-setup tracing when this module is imported
# This ensures tracing is enabled as early as possible
_tracing_status = setup_tracing()
