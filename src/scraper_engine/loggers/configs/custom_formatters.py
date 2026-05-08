import datetime
import json
import logging

STANDARD_ATTRS = {
    "name",
    "msg",
    "args",
    "levelname",
    "levelno",
    "pathname",
    "filename",
    "module",
    "exc_info",
    "exc_text",
    "stack_info",
    "lineno",
    "funcName",
    "created",
    "msecs",
    "relativeCreated",
    "thread",
    "threadName",
    "processName",
    "process",
    "message",
    "asctime",
    "taskName",
}


def format_timestamp(timestamp: float) -> str:
    datetime_object = datetime.datetime.fromtimestamp(timestamp, tz=datetime.UTC)
    return datetime_object.isoformat(timespec="milliseconds")


class JSONFormatter(logging.Formatter):
    def format(self, log_record: logging.LogRecord) -> str:
        logger_dict = {
            "time": format_timestamp(log_record.created),
            "logger_name": log_record.name,
            "logger_level": log_record.levelname,
            "module": log_record.module,
            "file_path": log_record.pathname,
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
        extras = {
            key: val for key, val in log_record.__dict__.items() if key not in STANDARD_ATTRS
        }
        logger_dict["extra"] = extras

        return json.dumps(logger_dict, default=str)


class TextFormatter(logging.Formatter):
    def format(self, log_record: logging.LogRecord) -> str:
        extra = {key: val for key, val in log_record.__dict__.items() if key not in STANDARD_ATTRS}
        return (f"{format_timestamp(log_record.created)} - {log_record.name} " 
                f"- {log_record.levelname} - {log_record.pathname} - LINE: {log_record.lineno} " 
                f"- {log_record.getMessage()} - {extra}")
