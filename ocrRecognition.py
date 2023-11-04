from typing import List
import Quartz
from Foundation import NSURL
import Vision
from common import ImageOCR, OCRResult

from imageManipulation import get_box_coordinates_from

def get_recognize_text_handler_for_image(input_image, results: List[OCRResult]):
    def handler(request, error):
        ocr_observations = request.results()
        
        for ocr_observation in ocr_observations:
            # Return the string of the top VNRecognizedText instance.
            recognized_text = ocr_observation.topCandidates_(1)[0]
            box_coordinates = get_box_coordinates_from(recognized_text, input_image)

            results.append({
                'text': recognized_text.string(), 
                'confidence': recognized_text.confidence(), 
                'box_coordinates': box_coordinates
                })

    
    return handler
        

def get_ocr_and_coordinates_from_image_with_path(img_path: str) -> List[OCRResult]:
    # Get the CIImage on which to perform requests.
    input_url = NSURL.fileURLWithPath_(img_path)
    input_image = Quartz.CIImage.imageWithContentsOfURL_(input_url)

    # Create a new image-request handler.
    request_handler = Vision.VNImageRequestHandler.alloc().initWithCIImage_options_(
            input_image, None
    )
    ocr_results = []

    recognize_text_handler = get_recognize_text_handler_for_image(input_image, ocr_results)

    # Create a new request to recognize text.
    request = Vision.VNRecognizeTextRequest.alloc().initWithCompletionHandler_(recognize_text_handler)

    # Perform the text-recognition request.
    error = request_handler.performRequests_error_([request], None)

    # Deallocate memory
    request_handler.dealloc()
    request.dealloc()

    return ocr_results


def get_ocr_from_images(images_path: List[str]) -> List[ImageOCR]:
    imagesOCR = []
    for image_path in images_path:
        imagesOCR.append({
            "ocr_and_coordinates": get_ocr_and_coordinates_from_image_with_path(image_path),
            "image_path": image_path
            })
    return imagesOCR

def get_text_from_ocr(document_ocr: List[ImageOCR]) -> str: 
	document_text = ""
	for page_ocr in document_ocr:
		for ocr_item in page_ocr["ocr_and_coordinates"]:
			document_text += ocr_item["text"] + "\n"
	return document_text
