import tkinter as tk

from typing import Union

__all__ = (
    'Interface'
)

class Interface:
    async def Menu(self)              -> tk.Menu:...
    async def Bots(self, main: tk.Tk) -> Union[None, bool]:...
    async def Start(self)             -> None:...
    def UpDate_Bot(self, Id: str)     -> None:...