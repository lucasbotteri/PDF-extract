
from typing import List
from Foundation import  NSRange
import Vision
import Quartz
from PIL import Image, ImageDraw
from PIL.Image import Image as ImageType


from common import BoxCoordinates, ImageOCR, some_value_extracted_present_on_ocr


def get_box_coordinates_from(recognized_text, input_image) -> BoxCoordinates:
	# Find the bounding-box observation for the string range.
	box_range = NSRange(0, len(recognized_text.string()))
	boxObservation = recognized_text.boundingBoxForRange_error_(box_range, None)

	# Get the normalized CGRect value.
	boundingBox = boxObservation[0].boundingBox()
	
	# Convert the rectangle from normalized coordinates to image coordinates.
	image_width, image_height = input_image.extent().size.width, input_image.extent().size.height
	rect = Vision.VNImageRectForNormalizedRect(boundingBox, image_width, image_height)

	min_x = Quartz.CGRectGetMinX(rect)
	max_x = Quartz.CGRectGetMaxX(rect)

	# The y coordinates need to be flipped
	min_y = input_image.extent().size.height - Quartz.CGRectGetMaxY(rect)
	max_y = input_image.extent().size.height - Quartz.CGRectGetMinY(rect)

	return {
		"min_x": min_x,
		"min_y": min_y,
		"max_x": max_x,
		"max_y": max_y
	}


def get_draw_image_with_ocr_boxes(page_ocr: ImageOCR, array_of_results: List[str]) -> ImageType:
	image = Image.open(page_ocr["image_path"])
	draw = ImageDraw.Draw(image)
	for ocr_and_coordinates in page_ocr["ocr_and_coordinates"]:
		ocr_text = ocr_and_coordinates["text"]

		is_some_value_present = some_value_extracted_present_on_ocr(array_of_results, ocr_text)
		outline = "yellow" if is_some_value_present else "black"

		box_coordinates = ocr_and_coordinates["box_coordinates"]
		min_x = box_coordinates["min_x"]
		min_y = box_coordinates["min_y"]
		max_x = box_coordinates["max_x"]
		max_y = box_coordinates["max_y"]

			# Draw the observation rect on the image
		draw.rectangle([(min_x, min_y),(max_x, max_y)],outline=outline, width=3)
	return image


def save_images_as_pdf_to_path(images: List[ImageType], output_path: str):
		image_as_RGB = []
		for image in images:
			image_as_RGB.append(image.convert('RGB'))
		image_list = image_as_RGB[1:] 
		image_list[0].save(output_path, save_all=True, append_images=image_list)