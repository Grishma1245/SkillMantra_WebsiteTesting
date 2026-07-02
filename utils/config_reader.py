"""
config_reader.py
----------------
Reads configuration from config/config.ini and allows environment variable
overrides via python-dotenv. Environment variables always win over INI values.

Priority order (highest → lowest):
  1. OS environment variables (set manually or via .env file)
  2. config.ini [DEFAULT] or section values
"""

import configparser
import os

from dotenv import load_dotenv

from utils.logger import get_logger

logger = get_logger(__name__)

# Load .env file from the project root (if it exists)
_DOTENV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path=_DOTENV_PATH, override=False)

_CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "config", "config.ini"
)

_config = configparser.ConfigParser()
_config.read(_CONFIG_PATH)

_ENV_SECTION = os.environ.get("TEST_ENV", "DEFAULT").upper()


def _get(key: str, fallback: str | None = None) -> str | None:
    """
    Retrieve a config value. Environment variables override INI file values.

    Args:
        key: The configuration key (e.g., 'base_url', 'browser').
        fallback: Value returned if the key is not found anywhere.

    Returns:
        The resolved string value, or fallback.
    """
    env_key = key.upper()
    env_val = os.environ.get(env_key)
    if env_val is not None:
        logger.debug("Config key '%s' resolved from environment variable: '%s'", key, env_val)
        return env_val

    try:
        section = _ENV_SECTION if _config.has_section(_ENV_SECTION) else "DEFAULT"
        value = _config.get(section, key)
        logger.debug("Config key '%s' resolved from config.ini [%s]: '%s'", key, section, value)
        return value
    except (configparser.NoSectionError, configparser.NoOptionError):
        logger.warning("Config key '%s' not found; using fallback: '%s'", key, fallback)
        return fallback


def get_base_url() -> str:
    return _get("base_url", "https://skillmantraedu.com")


def get_browser() -> str:
    return _get("browser", "chrome").lower()


def get_timeout() -> int:
    return int(_get("timeout", "20"))


def is_headless() -> bool:
    val = _get("headless", "false").lower()
    return val in ("true", "1", "yes")


def is_screenshot_on_failure() -> bool:
    val = _get("screenshot_on_failure", "true").lower()
    return val in ("true", "1", "yes")
