import re
from PIL import Image
import pytesseract
import pandas as pd

'''
Usage:
--psm <number>

eg. --psm 6

Page segmentation modes:
  0    Orientation and script detection (OSD) only.
  1    Automatic page segmentation with OSD.
  2    Automatic page segmentation, but no OSD, or OCR.
  3    Fully automatic page segmentation, but no OSD. (Default)
  4    Assume a single column of text of variable sizes.
  5    Assume a single uniform block of vertically aligned text.
  6    Assume a single uniform block of text.
  7    Treat the image as a single text line.
  8    Treat the image as a single word.
  9    Treat the image as a single word in a circle.
 10    Treat the image as a single character.
 11    Sparse text. Find as much text as possible in no particular order.
 12    Sparse text with OSD.
 13    Raw line. Treat the image as a single text line,
                        bypassing hacks that are Tesseract-specific.
'''

f = input('Enter file name: ')

configs = ['--psm 4 tessedit_char_whitelist=0123456789/C', '--psm 6 tessedit_char_whitelist=0123456789/C']
concat_items = []

common_pattern = input('Enter common pattern: ')
len_item = 11

for config in configs:
    text = pytesseract.image_to_string(Image.open(f),config=config)

    lst = set(text.split('\n'))

    query = re.compile(r'\d\d/\d\D\d/\d\d\d\d')     # \d = digit, \D = not a digit

    items = [query.findall(x)[0] for x in lst if query.findall(x) != []]
    items = ['%s%s'%(common_pattern,x[-(len_item-len(common_pattern)):]) for x in items]

    for item in items:
        concat_items.append(item)

    print(f'Config: {config}')
    print(f'Accurate matches: {len(items)}')

concat_df = pd.DataFrame({'Entry':list(set(concat_items))})
print(concat_df)

writer = pd.ExcelWriter('file.xlsx')
concat_df.to_excel(writer)
writer.save()