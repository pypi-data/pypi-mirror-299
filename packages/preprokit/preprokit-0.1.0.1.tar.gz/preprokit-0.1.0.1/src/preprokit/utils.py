import sys
from unicodedata import category

complex_punctuations =  [chr(i) for i in range(sys.maxunicode) if category(chr(i)).startswith("P")]
simple_punctuations = [char for char in '''!()-[]{};:'"\\,<>./?@#$%^&*_~''']

# def can_convert_to_float(s):
#     try:
#         float(s)
#         return True
#     except ValueError:
#         return False

def filter_row(row, filters):
    return any(value in filters for value in row)
