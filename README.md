# PDF and Image Merger

## Description

This Python script allows you to merge PDF files and images (JPEG, JPG, PNG) into a single PDF file. All PDF pages and images are resized to a standard width while maintaining their aspect ratios.

## Requirements

- Python 3.x
- PyPDF2
- Pillow
- ReportLab

## Installation

1. Make sure you have Python 3 installed. If not, you can download it from [here](https://www.python.org/downloads/).
2. Clone the repository or download the Python script.
3. Install required packages:

```bash
pip install PyPDF2 Pillow reportlab
```

## Usage

Save the script as `merge_files.py`.

To execute the script, navigate to the directory containing the script and run the following command in the terminal:

```bash
python merge_files.py path/to/files/folder NAME
```

- `path/to/files/folder`: Replace this with the path to the folder containing the PDF and/or image files you want to merge.
- `NAME`: Replace this with the name you want for the output PDF file. The output file will be saved as `NAME.pdf` in the same directory as the script.

### Example

For instance, if you have a folder named `documents` containing files you want to merge, and you want the output PDF to be named `Merged_Document.pdf`, execute the following command:

```bash
python merge_files.py documents Merged_Document
```

This will create a merged PDF file named `Merged_Document.pdf` in the directory where the script is located.

## Notes

- The script sorts files alphabetically before merging.
- The standard width used is 612 points, which corresponds to the width of a letter-sized paper.
- Files with unsupported extensions are ignored.
- Temporary files generated during the process are automatically deleted.

## Author

Fabian Lander