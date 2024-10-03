from rich import print
from ..logger import Logger
from ..types_ import Level

class rich(Logger):
  def __call__(self, *objs, level: Level = 'INFO'):
    print(*objs)