import logging.config
from importlib.resources import files
import yaml
import os


def create_dictconfig(
    raise_exceptions: bool = True,
) -> None:   
    config_file = files("scraper_engine").joinpath("loggers/logger_config.yaml")
    with config_file.open('r',encoding='utf-8') as file:
        config = yaml.safe_load(file)
    logging.config.dictConfig(config=config)
    logging.raiseExceptions = raise_exceptions
    