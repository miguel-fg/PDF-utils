import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame
import os


class FileWindow(ScrolledFrame):
    def __init__(self, parent: ttk.Window, files: tuple) -> None:
        super().__init__(master=parent, autohide=True, bootstyle="warning")

        # display files
        for index, file in enumerate(files):
            filename = os.path.basename(file)

            ttk.Label(master=self, text=f"{index + 1}:\t\t{filename}").pack(
                expand=True, fill="both"
            )

        self.pack(expand=True, fill="both")
