import logging.config

import yaml


def create_dictconfig(
    config_path: str = '../logger_config.yaml',
    raise_exceptions: bool = True,
):
    with open(config_path) as file:
        config = yaml.safe_load(file)
    logging.config.dictConfig(config=config)
    logging.raiseExceptions = raise_exceptions
