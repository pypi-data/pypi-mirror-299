from typing import Sequence
from dslog.types_ import Level

def default(*objs, level: Level) -> Sequence:
  return (f'[{level}]', *objs)

def level_color(level: Level):
  match level:
    case 'DEBUG': return 'blue'
    case 'INFO': return 'green'
    case 'WARNING': return 'yellow'
    case 'ERROR': return 'red'
    case 'CRITICAL': return 'bold red'

def click(*objs, level: Level) -> Sequence:
  import click
  col = level_color(level)
  return click.style(f'[{level}]', fg=col), *objs

def rich(*objs, level: Level) -> Sequence:
  col = level_color(level)
  return f'[{col}][{level}][/{col}]', *objs