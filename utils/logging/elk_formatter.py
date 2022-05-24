from datetime import datetime
from logging import LogRecord
from typing import Dict

from pythonjsonlogger import jsonlogger


class ElkJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record: Dict, record: LogRecord, message_dict: Dict):
        super(ElkJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['@timestamp'] = datetime.now().isoformat()
        log_record['level'] = record.levelname
        log_record['logger'] = record.name
