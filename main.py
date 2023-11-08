import os
import logging
from LLMInteraction import get_csv_from_document_text
from imageManipulation import get_draw_image_with_ocr_boxes, save_images_as_pdf_to_path
from pdf2image import convert_from_path
import sys
import tempfile
from ocrRecognition import get_ocr_from_images, get_text_from_ocr
import traceback


def visualize_results_for_document_ocr(document_ocr, array_of_results):
    for page_ocr in document_ocr:
        image_drawn = get_draw_image_with_ocr_boxes(page_ocr, array_of_results)
        image_drawn.show()


def save_results_as_pdf(document_ocr, array_of_results, output_path):
    images_drawn = []
    for page_ocr in document_ocr:
        image_drawn = get_draw_image_with_ocr_boxes(page_ocr, array_of_results)
        images_drawn.append(image_drawn)
    save_images_as_pdf_to_path(images_drawn, output_path)

if len(sys.argv) < 2:
    logging.error("Usage: python script.py <folder_path>")
    sys.exit(1)

folder_path = sys.argv[1]
print(f"The folder path is: {folder_path}")

files = os.listdir(folder_path)
pdf_files = [f for f in files if f.endswith('.pdf')]

with open('out/output.csv', 'w') as gpt_response:

    gpt_response.write('archivo, nombre_de_la_persona,numero_de_resolucion,numero_de_legajo,fecha_de_aplicacion')
    gpt_response.write('\n')
    for pdf_file in pdf_files:

        file_path = os.path.join(folder_path, pdf_file)
        file_name_no_extension = os.path.splitext(pdf_file)[0]
        print(f"Processing file: {file_path}")

        with tempfile.TemporaryDirectory() as path_to_save_images:
            

            images_paths = convert_from_path(file_path, paths_only = True, fmt="png", output_folder = path_to_save_images)
            document_ocr = get_ocr_from_images(images_paths)

            document_text = get_text_from_ocr(document_ocr)
            trimmed_document_text = document_text.replace('\n', '').replace('\t', '')

            try:
                csvResponse = get_csv_from_document_text(trimmed_document_text)
                csvResponseWithFilename = f"{pdf_file}, {csvResponse}" 
                gpt_response.write(csvResponseWithFilename)
                gpt_response.write('\n')       

                recognized_person_data = csvResponse.split(',')
                
                print(f"Recognized person data for {pdf_file}: {recognized_person_data}")


                save_results_as_pdf(document_ocr, recognized_person_data, f"out/{file_name_no_extension}_result.pdf")
            except Exception as e:
                logging.error(f"Error processing file {pdf_file}: {e}")
                logging.error(traceback.format_exc())
