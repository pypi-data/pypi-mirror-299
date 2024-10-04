# Documentation for Document Converter Code

This Python code provides a set of classes designed to extract text from various document formats: PDF, PPTX (PowerPoint), and DOCX (Word). It utilizes the `PyPDF2`, `python-pptx`, and `python-docx` libraries to accomplish this task. Below is a breakdown of each class and its methods.
To install this : 

`pip install doc-converter`
## Classes





### 1. `pdf`
The `pdf` class is responsible for extracting text from PDF files.

#### Methods
- **`__init__(self, path: str) -> None`**
  - **Parameters:**
    - `path`: The directory path where the PDF files are located.
  - **Description:** Initializes the class with the specified directory path.

- **`pdf_to_text(self) -> List[str]`**
  - **Returns:** A list of strings, each containing the text extracted from a PDF file.
  - **Description:** 
    - Changes the working directory to the specified path.
    - Scans for all PDF files in the directory.
    - Reads each PDF file and extracts text from all pages.
    - Returns a list containing the extracted text from each PDF file.

### 2. `pptx_files`
The `pptx_files` class is designed to extract text from PPTX (PowerPoint) files.

#### Methods
- **`__init__(self, path: str) -> None`**
  - **Parameters:**
    - `path`: The directory path where the PPTX files are located.
  - **Description:** Initializes the class with the specified directory path.

- **`pptx_to_text(self) -> List[str]`**
  - **Returns:** A list of strings, each containing the text extracted from a PPTX file.
  - **Description:**
    - Changes the working directory to the specified path.
    - Scans for all PPTX files in the directory.
    - Reads each PPTX file and extracts text from all slides and shapes.
    - Returns a list containing the extracted text from each PPTX file.

### 3. `DocxtoText`
The `DocxtoText` class is responsible for extracting text from DOCX (Word) files.

#### Methods
- **`__init__(self, path: str) -> None`**
  - **Parameters:**
    - `path`: The directory path where the DOCX files are located.
  - **Description:** Initializes the class with the specified directory path.

- **`docx_to_text(self) -> List[str]`**
  - **Returns:** A list of strings, each containing the text extracted from a DOCX file.
  - **Description:**
    - Changes the working directory to the specified path.
    - Scans for all DOCX files in the directory.
    - Reads each DOCX file and extracts text from all paragraphs.
    - Returns a list containing the extracted text from each DOCX file.

## Example Usage
To use these classes, instantiate the desired class with the appropriate path and call the corresponding text extraction method:

```python
# Example for extracting text from DOCX files
docx_converter = DocxtoText(path=r"C:\Users\Ibrahim.intern\Desktop\Converter")
docx_texts = docx_converter.docx_to_text()
print(len(docx_texts))  # Prints the number of DOCX files processed

# Example for extracting text from PDF files
pdf_converter = pdf(path=r"C:\Users\Ibrahim.intern\Desktop\Converter")
pdf_texts = pdf_converter.pdf_to_text()
print(len(pdf_texts))  # Prints the number of PDF files processed

# Example for extracting text from PPTX files
pptx_converter = pptx_files(path=r"C:\Users\Ibrahim.intern\Desktop\Converter")
pptx_texts = pptx_converter.pptx_to_text()
print(len(pptx_texts))  # Prints the number of PPTX files processed
```

## Requirements
To run this code, ensure that the following packages are installed:
- `python-docx`
- `python-pptx`
- `PyPDF2`

You can install these packages using pip:
```bash
pip install python-docx python-pptx PyPDF2
```

## Notes
- The code assumes that the specified directory contains files of the supported formats. If there are no files of a given format, an empty list will be returned for that format.
- Make sure to handle any potential exceptions that may arise when reading files, such as file access issues or file format errors.