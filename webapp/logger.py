import logging

import yaml
from gunicorn import glogging

with open('conf/logging.conf.yml', 'r') as f:
    LOGGING_CONFIG = yaml.load(f, Loader=yaml.FullLoader)


class UniformLogger(glogging.Logger):
    def setup(self, cfg):
        logging.config.dictConfig(LOGGING_CONFIG)
