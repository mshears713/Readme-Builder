"""Tracing and observability utilities for LangSmith and LangFuse."""

import logging
import os
from dataclasses import dataclass
from typing import Optional


logger = logging.getLogger(__name__)


@dataclass
class LangSmithDiagnostics:
    """Lightweight status report for LangSmith configuration."""

    enabled_flag: bool
    api_key_present: bool
    project_name: str
    endpoint: str
    client_ready: bool = False
    error_message: Optional[str] = None

    @property
    def status_label(self) -> str:
        if self.client_ready:
            return "ready"
        if not self.enabled_flag:
            return "disabled"
        if not self.api_key_present:
            return "missing_api_key"
        if self.error_message:
            return f"error: {self.error_message}"
        return "pending"


def describe_langsmith_status(diag: Optional[LangSmithDiagnostics] = None) -> str:
    """Return a friendly one-line summary describing LangSmith readiness."""

    diag = diag or collect_langsmith_diagnostics()

    status = f"LangSmith status → {diag.status_label}"
    details = [
        f"enabled={'yes' if diag.enabled_flag else 'no'}",
        f"api_key={'set' if diag.api_key_present else 'missing'}",
    ]

    if diag.enabled_flag:
        details.append(f"project={diag.project_name}")
        details.append(f"endpoint={diag.endpoint}")

    if diag.error_message:
        details.append(f"error={diag.error_message}")

    if diag.client_ready:
        details.append("client_ready=yes")

    return f"{status} ({', '.join(details)})"


def collect_langsmith_diagnostics() -> LangSmithDiagnostics:
    """Return the current LangSmith environment status without side effects."""

    enabled = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
    diag = LangSmithDiagnostics(
        enabled_flag=enabled,
        api_key_present=bool(os.getenv("LANGCHAIN_API_KEY", "")),
        project_name=os.getenv("LANGCHAIN_PROJECT", "project-forge"),
        endpoint=os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com"),
    )
    return diag


def initialize_langsmith_client(diag: Optional[LangSmithDiagnostics] = None) -> LangSmithDiagnostics:
    """Attempt to create a LangSmith client; never raises if configuration is missing."""

    diag = diag or collect_langsmith_diagnostics()

    if not diag.enabled_flag:
        logger.debug("LangSmith tracing disabled via environment flag.")
        return diag

    if not diag.api_key_present:
        diag.error_message = "LANGCHAIN_API_KEY not set"
        logger.warning("LangSmith tracing enabled but no API key found.")
        return diag

    try:
        from langsmith import Client
    except ImportError:
        diag.error_message = "langsmith package not installed"
        logger.warning("Install the 'langsmith' package to enable tracing.")
        return diag

    try:
        Client(
            api_key=os.getenv("LANGCHAIN_API_KEY"),
            api_url=diag.endpoint,
            project=diag.project_name,
        )
        diag.client_ready = True
        diag.error_message = None
        logger.info("LangSmith client initialized successfully.")
    except Exception as exc:  # pragma: no cover - defensive logging
        diag.error_message = str(exc)
        logger.error("LangSmith client initialization failed: %s", exc)

    return diag


def setup_langsmith_tracing() -> bool:
    """Set up LangSmith tracing if configured via environment variables."""

    diag = initialize_langsmith_client()
    if diag.client_ready:
        logger.info("LangSmith tracing enabled for project: %s", diag.project_name)
        logger.debug("LangSmith endpoint: %s", diag.endpoint)
        return True

    logger.debug("LangSmith tracing unavailable (%s)", diag.status_label)
    return False


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
    langchain_diag = collect_langsmith_diagnostics()
    langchain_diag = initialize_langsmith_client(langchain_diag) if langchain_diag.enabled_flag else langchain_diag

    langfuse_public_key = bool(os.getenv("LANGFUSE_PUBLIC_KEY", ""))
    langfuse_secret_key = bool(os.getenv("LANGFUSE_SECRET_KEY", ""))

    try:
        import langfuse  # noqa: F401
        langfuse_installed = True
    except ImportError:
        langfuse_installed = False

    return {
        "langsmith": {
            "enabled": langchain_diag.enabled_flag,
            "has_api_key": langchain_diag.api_key_present,
            "project": langchain_diag.project_name if langchain_diag.enabled_flag else None,
            "endpoint": langchain_diag.endpoint if langchain_diag.enabled_flag else None,
            "client_ready": langchain_diag.client_ready,
            "status": langchain_diag.status_label,
            "error": langchain_diag.error_message,
        },
        "langfuse": {
            "enabled": langfuse_public_key and langfuse_secret_key,
            "has_keys": langfuse_public_key and langfuse_secret_key,
            "host": os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com") if (langfuse_public_key and langfuse_secret_key) else None,
            "package_installed": langfuse_installed,
        },
    }
