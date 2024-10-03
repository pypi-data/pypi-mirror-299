import pkgutil
import sys

from scrapyd.config import Config
from scrapyd.exceptions import ConfigError
from scrapyd.utils import initialize_component

__version__ = pkgutil.get_data(__package__, "VERSION").decode().strip()
version_info = tuple(__version__.split(".")[:3])


def get_application(config=None):
    if config is None:
        config = Config()
    try:
        return initialize_component(config, "application", "scrapyd.app.application")
    except ConfigError as e:
        sys.exit(str(e))
