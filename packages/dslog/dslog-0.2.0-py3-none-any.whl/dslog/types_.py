from typing import Protocol, Literal, Sequence

Level = Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
LEVELS: Sequence[Level] = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
LEVEL_VALUES: dict[Level, int] = {
  'DEBUG': 10,
  'INFO': 20,
  'WARNING': 30,
  'ERROR': 40,
  'CRITICAL': 50,
}

def value(level: Level | int) -> int:
  return level if isinstance(level, int) else LEVEL_VALUES[level]

class Handler(Protocol):
  def __call__(self, *objs, level: Level):
    ...

class Formatter(Protocol):
  def __call__(self, *objs, level: Level) -> Sequence:
    ...
