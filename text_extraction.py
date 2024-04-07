###############################################################################
#### EXTRACT DATA FROM THE PDF FILES ####
###############################################################################
# code is from: https://github.com/zoumdatascience/OCR/blob/main/TextFromAnyPDF.ipynb
!pip install pdf2image
!pip install pytesseract


from pdf2image import convert_from_path
from pytesseract import image_to_string
from PIL import Image

# since the invoices and the bank statements are scanned PDF we need to prepare the data so that we can extract the data

#convert pdf to image, returns an iterable containing image format of all the pages of the pdf
def convert_pdf_to_img(pdf_file):
    return convert_from_path(pdf_file)

# convert image to text, returns the textual content of a single image
def convert_image_to_text(file):    
    text = image_to_string(file)
    return text

# combining the two previous functions, returns the textual content of all pages
def get_text_from_any_pdf(pdf_file):
    images = convert_pdf_to_img(pdf_file)
    final_text = ""
    for pg, img in enumerate(images):
        
        final_text += convert_image_to_text(img)
        #print("Page n°{}".format(pg))
        #print(convert_image_to_text(img))
    
    return final_text

# Testing with one document
pdf_file = '/Users/alessandracerutti/ucl-invoice-assistant/data/invoice_scan/invoice_1.pdf'
text = get_text_from_any_pdf(pdf_file)

# Printing result in terminal to see if it is correct
print(text)

# Compared to the original document
# Facture number is correct 
# Adress has only one error (correct would be: "Pl. de la" instead of "Pl. de la B")
# Total amount is not extracted
# Date is correctly extracted 