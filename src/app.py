import tkinter as tk
import ttkbootstrap as ttk


class App(ttk.Window):
    def __init__(self, title: str, dimensions: tuple):
        super().__init__(themename="minty")

        # app setup
        self.title(title)
        self.geometry(f"{dimensions[0]}x{dimensions[1]}")
        self.minsize(width=dimensions[0], height=dimensions[1])

        # labels
        self.app_title = ttk.Label(
            master=self,
            text="PDF utils",
            anchor="center",
            bootstyle="inverse-light",
            font=("Helvetica Bold", 40),
        )
        self.label = ttk.Label(
            master=self,
            text="choose any of the tools available",
            anchor="center",
            bootstyle="default",
            font=("Helvetica", 15),
        )

        self.app_title.pack(fill="x")
        self.label.pack(fill="x")

        # option grid
        self.options = self.options_frame(parent=self)
        self.options.pack(expand=True, fill="both", padx=200, pady=100)

        # run
        self.mainloop()

    def options_frame(self, parent: ttk.Window) -> ttk.Frame:
        frame = ttk.Frame(master=parent)

        # grid layout
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure((0, 1, 2), weight=1, uniform="a")

        # option buttons
        merge_btn = ttk.Button(
            master=frame,
            text="Merge",
            command=self.merge_selected,
            bootstyle="primary",
        )
        split_btn = ttk.Button(
            master=frame,
            text="Split",
            command=self.split_selected,
            bootstyle="secondary", 
        )
        compress_btn = ttk.Button(
            master=frame,
            text="Compress",
            command=self.compress_selected,
            bootstyle="info",
        )

        merge_btn.grid(row=0, column=0, sticky="nsew", padx=10, pady=200)
        split_btn.grid(row=0, column=1, sticky="nsew", padx=10, pady=200)
        compress_btn.grid(row=0, column=2, sticky="nsew", padx=10, pady=200)

        return frame

    # create Merge menu
    def merge_selected(self) -> None:
        # clean the window
        self.app_title.pack_forget()
        self.label.pack_forget()
        self.options.pack_forget()

    # create Split menu
    def split_selected(self) -> None:
        # clean the window
        self.app_title.pack_forget()
        self.label.pack_forget()
        self.options.pack_forget()

    # create Compress menu
    def compress_selected(self) -> None:
        # clean the window
        self.app_title.pack_forget()
        self.label.pack_forget()
        self.options.pack_forget()

class MergeWindow(ttk.Frame):
    def __init__(self, parent: ttk.Window) -> None:
        super().__init__(master=parent)
        

App("PDF utilities", (1600, 900))
