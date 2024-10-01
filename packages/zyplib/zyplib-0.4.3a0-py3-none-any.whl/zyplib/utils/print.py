from typing import Literal

COLOR_MAP = {
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'magenta': '\033[95m',
    'cyan': '\033[96m',
    'white': '\033[97m',
    'reset': '\033[0m',
}


COLOR_TYPE = Literal['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']


def colored(text: str, color: COLOR_TYPE):
    """为文本添加颜色


    Parameters
    ----------
    - `text` : `str`
        - 原始文本
    - `color` : `COLOR_TYPE`
        - 颜色类型
        - `"red"` | `"green"` | `"yellow"` | `"blue"` | `"magenta"` | `"cyan"` | `"white"`
    """
    return f"{COLOR_MAP[color]}{text}{COLOR_MAP['reset']}"


def print_colored(color: COLOR_TYPE, *args, **kwargs):
    """打印带颜色的文本

    Parameters
    ----------
    - `color` : `COLOR_TYPE`
        - 颜色类型
        - `"red"` | `"green"` | `"yellow"` | `"blue"` | `"magenta"` | `"cyan"` | `"white"`
    """

    total_text = ' '.join([str(arg) for arg in args])
    print(colored(total_text, color), **kwargs)
