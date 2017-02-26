import io
import os

# Imports the Google Cloud client library
from google.cloud import vision

path = '/Users/akshungupta/git/Hackillinois2017/ocr/test.png'

def detect_text(path):
	"""Detects text in the file."""
	vision_client = vision.Client()

	with io.open(path, 'rb') as image_file:
	    content = image_file.read()

	image = vision_client.image(content=content)

	texts = image.detect_text()
	print('Texts:')
	# for text in texts:
	#     # print(text.description)
	#     # split = 
	#     if (len(text.description) != 0):
	#     	print(text.description)

	result = [text.description for text in texts]
	index_medicine = result.index("Medicine:")
	result = result[index_medicine:]
	print(result)

	return result
	    

detect_text(path)