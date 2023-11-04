
from typing import TypedDict, List

def some_value_extracted_present_on_ocr(array_of_strings: List[str], search_string: str) -> bool:
    # Check each element in each sub-array for the search_string
    return any(str(element) in search_string for element in array_of_strings)

class BoxCoordinates(TypedDict):
    min_x: int
    min_y: int
    max_x: int
    max_y: int
    
class OCRResult(TypedDict):
	text: str
	confidence: float
	box_coordinates: BoxCoordinates
    
class ImageOCR(TypedDict):
	ocr_and_coordinates: List[OCRResult]
	image_path: str