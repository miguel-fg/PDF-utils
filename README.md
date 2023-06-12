# PDF tools
The PDF tools application is a Python Tkinter-based desktop application that allows you to merge, split, and compress PDF files. It provides a simple and intuitive user interface and utilizes the Bootstrap Tkinter library for enhanced styling. The application uses the PyPDF2 and PyMuPDF libraries for PDF file handling.

## Features
* Merge multiple PDF files into a single PDF file.
* Split a single PDF file into two PDF files after a specific page.
* PDF lossless compression
* User-firendly interface with `ttkbootstrap` styling.
* File preview sidebar.
* Toast notifications after completing a task.

## Requirements
* Python 3.6+
* `tkinter` library (included in most Python distributions) 
* `PyPDF2` library (https://pypi.org/project/PyPDF2/)
* `PyMuPDF` library (https://pymupdf.readthedocs.io/en/latest/)
* `ttkbootstrap` library (https://ttkbootstrap.readthedocs.io/en/latest/)

## Installation
1. Ensure that you have Python 3 installed on your system. You can download it from the official Python website: https://www.python.org/downloads/
2. Install the required Python libraries by running the following commands in your terminal or command prompt (the use of a virtual environment is highly recommended):
  ```shell
  python -m pip install --upgrade pymupdf
  python -m pip install pypdf2
  python -m pip install ttkbootstrap
  ```
3. Clone or download the source code from this GitHub repository.

## Usage
Navigate to the project directory and run the following command in your terminal or command prompt to start the application:
```shell
  python app.py
  ```
Once the application starts you can use the buttons and options provided to perform the desired operations:
* To merge PDF files, click the "Merge" button, select the input PDF files in desired merge order, optionally, flip the switch to reverse the order. Click the merge button again to finish the operation.
* To split a PDF file, click the "Split" button, select the input PDF file, select the page after which you wish to split the file from the dropdown menu. Click the split button again to finish the operation.
* To compress a PDF file, click the "Compress" button, select the input PDF file and click the compress button again to finish the operation.
* The output file(s) can be found in the app's folder. 

## Future improvements
* Will add multiple split points to the Split function.
* Will add multiple compression levels to the Compression function.
* GUI modernization is in the works.
