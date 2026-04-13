import json
import logging


class JsonFormatter(logging.Formatter):
    def format(self, log_record: logging.LogRecord) -> str:
        logger_dict = {
            "time": log_record.created,
            "logger_name": log_record.name,
            "logger_level": log_record.levelname,
            "module": record.module,
            "file_path": record.pathname,
            "function": log_record.funcName,
            "logger_line": log_record.lineno,
            "message": log_record.getMessage(),
            "stack_trace": self.formatStack(log_record.stack_info)
            if log_record.stack_info
            else None,
            "exception_info": self.formatException(log_record.exc_info)
            if log_record.exc_info
            else None,
        }

        return json.dumps(logger_dict)
