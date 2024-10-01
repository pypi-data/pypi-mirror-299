from netbox_negistry_importer import __appname__

from dynaconf import Dynaconf
from dynaconf import Validator

from loguru import logger
import appdirs
import os

os.environ["XDG_CONFIG_DIRS"] = "/etc"
config_files = ['settings.yaml', '.secrets.yaml']
USER_CONFIG_FILES = [os.path.join(appdirs.user_config_dir(
    __appname__), file) for file in config_files]
ROOT_CONFIG_FILES = [os.path.join(appdirs.site_config_dir(
    __appname__), file) for file in config_files]

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=config_files,
    includes=ROOT_CONFIG_FILES + USER_CONFIG_FILES
)

logger.debug(
    f"Configuration files load from {settings.ROOT_PATH_FOR_DYNACONF}")

# Register validators
settings.validators.register(
    # Ensure some parameters exists (are required)
    Validator('NETBOX_API_TOKEN', 'NETBOX_INSTANCE_URL',
              'NEGISTRY_URL', must_exist=True),
)

# Fire the validator
try:
    settings.validators.validate()
except Exception as e:
    logger.exception(e)
    logger.debug(settings.items())
    logger.error(f"Invalid configuration.\n{e}\nExiting....")
    exit(1)
