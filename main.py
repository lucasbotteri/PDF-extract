import os
from imageManipulation import get_draw_image_with_ocr_boxes
from pdf2image import convert_from_path
import sys
import tempfile
from ocrRecognition import get_ocr_from_images, get_text_from_ocr


def visualize_results_for_document_ocr(document_ocr, array_of_results):
    for page_ocr in document_ocr:
        image_drawn = get_draw_image_with_ocr_boxes(page_ocr, array_of_results)
        image_drawn.show()



if len(sys.argv) < 2:
    print("Usage: python script.py <folder_path>")
    sys.exit(1)

folder_path = sys.argv[1]
print(f"The folder path is: {folder_path}")

files = os.listdir(folder_path)
pdf_files = [f for f in files if f.endswith('.pdf')]

with open('output.csv', 'w') as gpt_response:

    gpt_response.write('nombre_de_la_persona,numero_de_resolucion,numero_de_legajo,fecha_de_aplicacion')
    gpt_response.write('\n')
    for pdf_file in pdf_files:

        file_path = os.path.join(folder_path, pdf_file)
        print(f"Processing file: {file_path}")

        with tempfile.TemporaryDirectory() as path_to_save_images:

            images_paths = convert_from_path(file_path, paths_only = True, fmt="png", output_folder = path_to_save_images)
            document_ocr = get_ocr_from_images(images_paths)

            document_text = get_text_from_ocr(document_ocr)
            trimmed_document_text = document_text.replace('\n', '').replace('\t', '')

            """
            # Chatgpt integration


            gpt_response.write(csvResponse)
            gpt_response.write('\n')       

            gpt_recognized_person_data = csvResponse.split(',')
            """
            

            gpt_recognized_person_data = ['Mariel Viviana MASTRI', 'RESO-2023-3786-GDEBA-MSALGP', '326.874', '12 de mayo de 2023']
            visualize_results_for_document_ocr(document_ocr, gpt_recognized_person_data)