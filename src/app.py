import tkinter as tk
import ttkbootstrap as ttk
from tkinter import filedialog as fd
import file_window as fw


# main app
class App(ttk.Window):
    def __init__(self, title: str, dimensions: tuple) -> None:
        super().__init__(themename="minty")
        # app setup
        self.title(title)
        self.geometry(f"{dimensions[0]}x{dimensions[1]}")
        self.minsize(width=1000, height=800)
        # main menu layout
        self.main_menu()

        # run
        self.mainloop()

    # Main menu of the app, user selects task to perform
    def main_menu(self) -> None:
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

    # option buttons
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

        title_label = ttk.Label(
            master=self, text="Merge", font=("Helvetica", 40), anchor="center"
        )

        TaskWindow(self, title_label)

    # create Split menu
    def split_selected(self) -> None:
        # clean the window
        self.app_title.pack_forget()
        self.label.pack_forget()
        self.options.pack_forget()

        title_label = ttk.Label(
            master=self, text="Split", font=("Helvetica", 40), anchor="center"
        )

        TaskWindow(self, title_label)

    # create Compress menu
    def compress_selected(self) -> None:
        # clean the window
        self.app_title.pack_forget()
        self.label.pack_forget()
        self.options.pack_forget()

        title_label = ttk.Label(
            master=self, text="Compress", font=("Helvetica", 40), anchor="center"
        )

        TaskWindow(self, title_label)


# window to perform a selected task on a PDF file
class TaskWindow(ttk.Frame):
    def __init__(self, parent: ttk.Window, title_label: ttk.Label) -> None:
        super().__init__(master=parent)

        # window title
        self.title_label = title_label
        self.title_label.pack(fill="x")

        # inner frame
        self.import_frame = ttk.Frame(master=self)
        self.import_frame.pack(expand=True, fill="both")

        # File Import button
        FileImport(self.import_frame)

        # back button
        self.back_button = ttk.Button(
            master=self, text="Back", command=lambda: self.go_back(parent)
        )
        self.back_button.pack()

        self.pack(expand=True, fill="both")

    # back to main menu button
    def go_back(self, p: ttk.Window) -> None:
        # clean the window and goes back to main menu
        self.title_label.pack_forget()
        self.pack_forget()
        p.main_menu()


# class to import files
class FileImport(ttk.Frame):
    def __init__(self, parent: ttk.Frame) -> None:
        super().__init__(master=parent)

        # dialog box trigger button
        self.button = ttk.Button(
            master=self,
            text="Import Files",
            command=lambda: self.import_files(parent),
            bootstyle="danger",
        )
        self.button.pack(pady=10)

        self.pack()

    # open dialog box and store the selected files in a tuple
    def import_files(self, p: ttk.Frame) -> tuple:
        filetypes = (("PDFs", "*.pdf"), ("All files", "*.*"))

        files = fd.askopenfilenames(
            title="Import files", initialdir="/", filetypes=filetypes
        )

        if len(files) > 0:
            self.pack_forget()
            fw.FileWindow(p, files)

        return files


App("PDF utilities", (1600, 900))
