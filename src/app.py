# GUI
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import filedialog as fd
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.toast import ToastNotification

# filename manipulation
import os

# image rendering
from PIL import Image, ImageTk

# PDF tools
import fitz
from PyPDF2 import PdfReader, PdfWriter


# main app
class App(ttk.Window):
    def __init__(self, title: str, dimensions: tuple) -> None:
        super().__init__(themename="simplex")

        # app setup
        self.title(title)
        self.geometry(f"{dimensions[0]}x{dimensions[1]}")
        self.minsize(width=1300, height=700)

        # main menu layout
        self.main_menu()

        # run
        self.mainloop()

    # Main menu of the app, user selects task to perform
    def main_menu(self) -> None:
        # creates a clean cache folder for GUI display images
        if not os.path.exists("src\.imgcache"):
            os.makedirs("src\.imgcache")
        else:
            for img in os.scandir("src\.imgcache"):
                os.remove(img.path)

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
            bootstyle="primary",
        )
        compress_btn = ttk.Button(
            master=frame,
            text="Compress",
            command=self.compress_selected,
            bootstyle="primary",
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
        self.title_label.pack(fill="x", pady=(5, 20))

        # inner frame
        self.import_frame = ttk.Frame(master=self)
        self.import_frame.pack(expand=True, fill="both")

        # File Import button
        FileImport(self.import_frame, title_label["text"])

        # back button
        self.back_button = ttk.Button(
            master=self,
            text="Back",
            command=lambda: self.go_back(parent),
            bootstyle="primary",
            width=40,
        )
        self.back_button.pack(pady=(0, 20))

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
            bootstyle="warning",
            width=50,
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
        self.total_img = []
        self.images = []
        self.file_images_display = ScrolledFrame(
            master=self.panel, autohide=True, bootstyle="light"
        )

        # table view to display files in use and their info
        headers = [
            {"text": "ID", "stretch": False},
            {"text": "File name", "stretch": False},
            {"text": "Pages", "stretch": True},
            {"text": "Size", "stretch": True},
        ]

        self.dt = Tableview(master=self, coldata=headers, bootstyle="light")

        # display files in main window
        for index, file in enumerate(files):
            filename = os.path.basename(file)
            size_mb = os.stat(file).st_size / (1024**2)

            if size_mb < 1:
                size_kb = size_mb * 1024
                size = f"{round(size_kb, 4)} Kb"
            else:
                size = f"{round(size_mb, 4)} Mb"

            with open(file, "rb") as f:
                reader = PdfReader(f)
                self.dt.insert_row("end", [index, filename, len(reader.pages), size])
                self.dt.load_table_data()

            self.images = self.extract_images(index, file)

            for img in self.images:
                self.total_img.append(img)

        self.dt.place(relwidth=0.78, relheight=0.8)

        # display files in side panel
        for img in self.total_img:
            ttk.Label(
                master=self.file_images_display,
                image=img,
                anchor="center",
            ).pack(pady=5)

        self.file_images_display.pack(expand=True, fill="both")

        # options according to the task
        self.extra_options(task, files)

        # button to trigger the task
        ttk.Button(
            master=self.panel,
            text=task,
            command=lambda: self.task(task, files),
            bootstyle="warning",
        ).pack(fill="x", padx=10, pady=5)

        self.panel.animate_forward()  # panel slides into the app

        self.pack(expand=True, fill="both")

    # extra options layout
    def extra_options(self, task: str, files: tuple):
        # add reverse checkbox for the Merge task
        if task == "Merge":
            self.checkVar = tk.IntVar(value=0)
            self.reverse_check = ttk.Checkbutton(
                master=self.panel,
                text="       Reverse order",
                bootstyle="info-square-toggle",
                variable=self.checkVar,
            )
            self.reverse_check.pack(pady=10)

        # Add split point menu button to the Split task
        elif task == "Split":
            doc = fitz.open(files[0])

            self.split_point = ttk.Menubutton(
                master=self.panel,
                text="Split after page: ",
                bootstyle="info",
            )

            pages = tk.Menu(self.split_point)

            # counting the number of pages in the document and adding them as options for the Menubutton
            self.split_option = tk.IntVar(value=1)
            counter = 0
            for page in doc:
                counter += 1
                pages.add_radiobutton(
                    label=str(counter), value=counter, variable=self.split_option
                )

            self.split_point["menu"] = pages

            self.split_point.pack(pady=10)

    # action to perform
    def task(self, task: str, files: tuple):
        self.panel.animate_backwards()  # move panel backwards

        if task == "Merge":
            merger = PdfWriter()

            if self.checkVar.get() == 1:
                files = reversed(files)

            for file in files:
                merger.append(file)

            with open("merged.pdf", "wb") as out:
                merger.write(out)

        elif task == "Split":
            pivot = self.split_option.get()

            with open(files[0], "rb") as infile:
                reader = PdfReader(infile)
                writer2 = PdfWriter()
                writer1 = PdfWriter()

                num_pages = reader._get_num_pages()

                for i in range(0, pivot):
                    writer1.add_page(reader.pages[i])

                for i in range(pivot, num_pages):
                    writer2.add_page(reader.pages[i])

                with open("split1.pdf", "wb") as out1:
                    writer1.write(out1)

                with open("split2.pdf", "wb") as out2:
                    writer2.write(out2)

        elif task == "Compress":
            with open(files[0], "rb") as infile:
                reader = PdfReader(infile)
                writer = PdfWriter()

                for page in reader.pages:
                    page.compress_content_streams()
                    writer.add_page(page)

                with open("compressed.pdf", "wb") as out:
                    writer.write(out)

        self.task_complete(task)

    # extract pdf page images
    def extract_images(self, filenum: int, filepath: str) -> list:
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

    # task complete notification
    def task_complete(self, task: str) -> None:
        verb = ""

        if task == "Merge":
            verb = "merged"
        elif task == "Split":
            verb = "split"
        else:
            verb = "compressed"

        self.toast = ToastNotification(
            title=f"Files {verb} successfully",
            message=f"Output file at {os.getcwd()}",
            duration=5000,
            bootstyle="success",
            position=(100,100, "se")
        )

        self.toast.show_toast()


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
        self.place(relx=start_pos, rely=0, relwidth=self.width, relheight=0.9)

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
            self.place(relx=self.pos, rely=0, relwidth=self.width, relheight=0.9)
            self.after(10, self.animate_forward)
        else:
            self.in_start_pos = False

    # moves the panel back
    def animate_backwards(self) -> None:
        if self.pos < self.start_pos:
            self.pos += 0.008
            self.place(relx=self.pos, rely=0, relwidth=self.width, relheight=0.9)
            self.after(10, self.animate_backwards)
        else:
            self.in_start_pos = True


App("PDF utilities", (1300, 700))
