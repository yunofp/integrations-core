from dynaconf import FlaskDynaconf
import os
import logging
logger = logging.getLogger(__name__)
def init_app(app):
    env = os.getenv('ENV_FOR_DYNACONF', 'default')
    settings_files = [f'settings.toml', f'settings.{env}.toml', '.secrets.toml']
    FlaskDynaconf(app, settings_files=settings_files)
    logger.info(f"Environment: {os.getenv('ENV_FOR_DYNACONF')}")
    logger.info(f"Settings files: {app.config._loaded_files}")
