import logging
from .logger import Logger, Formatter, Handler, Level, value

class StdHandler(logging.Handler):
  """A `logging.Handler` from a `dslog.Logger`"""
  def __init__(self, logger: Logger):
    super().__init__()
    self.logger = logger

  def emit(self, record):
    self.logger(record, level=record.levelname) # type: ignore (level)

def handler(logger: logging.Logger) -> Handler:
  def bound(*logs, level: Level):
    logger.log(value(level), ' '.join(str(obj) for obj in logs)) # `logging` is not the smartest library ever, tbh
  return bound

class StdFormatter(Formatter):

  def __init__(self, formatter: logging.Formatter):
    self._formatter = formatter
  
  def __call__(self, *record, level):
    return self._formatter.format(record), # type: ignore