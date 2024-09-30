import ctypes
from os import name, system
from sys import stdout, exc_info
from typing import Callable, Any

from .ansi import *


__all__ = ['System', 'sys']



class System:
    writefunc: Callable[[str], Any]
    """The function that is called when ANSI codes or text should be printed"""
    windows: bool
    """If the current operating system is Windows"""
    clear_at_end: bool
    """If the system should clear the terminal when the script stop"""
    
    def __init__(self, writefunc: Callable[[str], Any] | None = None) -> None:
        self.writefunc = writefunc or stdout.write
        self.windows = name == 'nt'
        self.clear_at_end = False
        self.__cursor = True
        self.__title = ''
        self.__transparency = -1

        if self.windows:
            self.__console = ctypes.windll.kernel32.GetConsoleWindow()
        else:
            self.__console = None


    def __del__(self) -> None:
        if self.clear_at_end:
            self.clear()

        self.writefunc(RESET)
        self.cursor = True


    @property
    def title(self) -> str:
        """The title of the terminal"""
        return self.__title


    @property
    def size(self) -> tuple[int, int]:
        """The size of the terminal (x, y)"""
        return self._size


    @property
    def cursor(self) -> bool:
        """if the cursor is activated in the terminal"""
        return self.__cursor


    @property
    def transparency(self) -> int:
        """The transparency of the terminal in byte"""
        return self.__transparency


    @title.setter
    def title(self, value: str) -> None:
        self.writefunc(TITLE.format(value))
        self.__title = value


    @size.setter
    def size(self, value: tuple[int, int]) -> None:
        if self.windows:
            system('mode {}, {}'.format(*value))
            self._size = value


    @cursor.setter
    def cursor(self, value: bool) -> None:
        self.writefunc(CURSOR if value else NO_CURSOR)
        self.__cursor = value


    @transparency.setter
    def transparency(self, value: int) -> None:
        if self.windows:
            ctypes.windll.user32.SetLayeredWindowAttributes(self.__console, 0, value, 2)
            self.__transparency = value


    def clear(self) -> None:
        """
        Clear all the text in the terminal.
        """
        self.writefunc(CLEAR)
        # TODO: stdout.flush()


sys: System = System()