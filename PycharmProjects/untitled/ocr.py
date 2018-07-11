from PIL import Image
from pytesseract import *
import sys

def OCR(img, lang ='jpn'):
    im =Image.open(img)
    test = image_to_string(im,lang=lang)
    print(test)
    return test

k = OCR('z.jpg')
t = sys.getsizeof(k)

print(t)
