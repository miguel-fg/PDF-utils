# GUI
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import filedialog as fd
from ttkbootstrap.scrolled import ScrolledFrame

# filename manipulation
import os

# image rendering
from PIL import Image, ImageTk

# PDF tools
import fitz


# main app
class App(ttk.Window):
    def __init__(self, title: str, dimensions: tuple) -> None:
        super().__init__(themename="morph")

        # creates a clean cache folder for GUI display images
        if not os.path.exists("src\.imgcache"):
            os.makedirs("src\.imgcache")
        else:
            for img in os.scandir("src\.imgcache"):
                os.remove(img.path)

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
            bootstyle="default",
            font=("Helvetica Bold", 40),
        )
        self.label = ttk.Label(
            master=self,
            text="choose any of the tools available",
            anchor="center",
            bootstyle="default",
            font=("Helvetica", 15),
        )

        self.app_title.pack(fill="x", pady=5)
        self.label.pack(fill="x")

        # option grid
        self.options = self.options_frame(parent=self)
        self.options.pack(expand=True, fill="both", padx=100, pady=100)

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

        merge_btn.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        split_btn.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        compress_btn.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

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
        FileImport(self.import_frame, title_label["text"])

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
    def __init__(self, parent: ttk.Frame, task: str) -> None:
        super().__init__(master=parent)

        # dialog box trigger button
        self.button = ttk.Button(
            master=self,
            text="Import Files",
            command=lambda: self.import_files(parent, task),
            bootstyle="danger",
        )
        self.button.pack(pady=10)

        self.pack()

    # open dialog box and store the selected files in a tuple
    def import_files(self, p: ttk.Frame, task: str) -> tuple:
        filetypes = (("PDFs", "*.pdf"), ("All files", "*.*"))

        files = fd.askopenfilenames(
            title="Import files", initialdir="/", filetypes=filetypes
        )

        if len(files) > 0:
            self.pack_forget()

            FileWindow(p, files, task)

        return files


# class to visualize file changes
class FileWindow(ScrolledFrame):
    def __init__(self, parent: ttk.Window, files: tuple, task: str) -> None:
        super().__init__(master=parent, autohide=True, bootstyle="default")

        self.panel = SlidePanel(parent, 1, 0.8)  # side panel instance

        # this will hold the file page images
        self.images = []
        self.file_images_display = ScrolledFrame(
            master=self.panel, autohide=True, bootstyle="secondary"
        )

        # display files in main window
        for index, file in enumerate(files):
            filename = os.path.basename(file)

            ttk.Label(master=self, text=f"{index + 1}:\t\t{filename}").pack(
                expand=True, fill="both"
            )

            self.images = self.extract_images(index, file)

        # display files in side panel
        for img in self.images:
            ttk.Label(
                master=self.file_images_display,
                image=img,
                anchor="center",
            ).pack(pady=5)

        self.file_images_display.pack(expand=True, fill="both")

        # button to trigger the task
        ttk.Button(
            master=self.panel, text="Something", command=lambda: self.task(task, files)
        ).pack(expand=True, fill="both")

        self.panel.animate_forward()  # panel slides into the app

        self.pack(expand=True, fill="both")

    # action to perform
    def task(self, task: str, files: tuple):
        self.panel.animate_backwards()  # move panel backwards

        if task == "Merge":
            basedoc = fitz.open(files[0])

            if len(files) > 1:
                for i in range(1, len(files)):
                    doc = fitz.open(files[i])
                    basedoc.insert_pdf(doc)
            
            basedoc.save("output.pdf")

        elif task == "Split":
            print("I split things :D")
        elif task == "Compress":
            print("I compressed things :D")

    # extract pdf page images
    def extract_images(self, filenum: int, filepath: str):
        doc = fitz.open(filepath)
        imgs = []
        w = 250
        h = 325

        # save images and generate cache
        for page in doc:
            pix = page.get_pixmap()
            pix.save(f"src\.imgcache\\f{filenum}-page-{page.number}.png")

            image_original = Image.open(
                f"src\.imgcache\\f{filenum}-page-{page.number}.png"
            ).resize((w, h))
            image_tk = ImageTk.PhotoImage(image_original)
            imgs.append(image_tk)

        return imgs


# animated side panel
class SlidePanel(ttk.Frame):
    def __init__(self, parent, start_pos, end_pos) -> None:
        super().__init__(master=parent)

        # general attributes
        self.start_pos = start_pos
        self.end_pos = end_pos - 0.01

        self.width = abs(start_pos - end_pos)

        # animation logic
        self.pos = start_pos
        self.in_start_pos = True

        # layout
        self.place(relx=start_pos, rely=0.05, relwidth=self.width, relheight=0.9)

    # check which way to animate
    def animate(self) -> None:
        if self.in_start_pos:
            self.animate_forward()
        else:
            self.animate_backwards()

    # calls the function up to the defined end position
    def animate_forward(self) -> None:
        if self.pos > self.end_pos:
            self.pos -= 0.008
            self.place(relx=self.pos, rely=0.05, relwidth=self.width, relheight=0.9)
            self.after(10, self.animate_forward)
        else:
            self.in_start_pos = False

    # moves the panel back
    def animate_backwards(self) -> None:
        if self.pos < self.start_pos:
            self.pos += 0.008
            self.place(relx=self.pos, rely=0.05, relwidth=self.width, relheight=0.9)
            self.after(10, self.animate_backwards)
        else:
            self.in_start_pos = True


App("PDF utilities", (1600, 900))
