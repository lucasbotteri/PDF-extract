## Description

This Python command application is a personal project designed to tackle a specific task of extracting information from lengthy PDFs issued by a government organization. While this application is tailored to my specific needs, it could serve as a useful reference or starting point for others with similar requirements.

### Key Functions:

- **Data Extraction**: Automatically identifies and extracts personal information.
- **CSV Generation**: Compiles the extracted data from all provided PDFs into a structured CSV file.
- **Visual Validation**: Generates images of the original PDFs with the extracted data highlighted.

## How It Works

1. **PDF Processing**:

   - The application starts by locating all PDF files in the `/files` folder.
   - Each page of every PDF file is converted into an image to facilitate OCR processing.

2. **Text Extraction with Apple Vision API**:

   - Using the Apple Vision API, accessed through PyObjC as a bridge between Python and Objective-C, the application performs OCR on the images.
   - The OCR process extracts the text content from each image.

3. **Data Extraction with GPT-3.5 Turbo**:

   - The extracted text from each page is compiled into a single prompt, including specific instructions for data extraction.
   - This prompt is sent to GPT-3.5 Turbo, which processes the text and identifies the relevant personal information.

4. **CSV Generation**:

   - The extracted personal information is saved to a CSV file. This file serves as a comprehensive list of all identified data from the processed PDFs.

5. **Visual Validation**:
   - To ensure the accuracy of the extracted data, the application generates images of the original PDF pages with the lines containing the extracted data highlighted.
   - These images are saved, allowing for manual validation and verification of the extraction process.
