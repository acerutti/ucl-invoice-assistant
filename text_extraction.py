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
pdf_file = '/Users/alessandracerutti/ucl-invoice-assistant/data/invoice_scan/invoice_2.pdf'

text = get_text_from_any_pdf(pdf_file)

# Printing result in terminal to see if it is correct
print(text)

# Compared to the original document
# Facture number is correct 
# Adress has only one error (correct would be: "Pl. de la" instead of "Pl. de la B")
# Total amount is not extracted
# Date is correctly extracted 

###### 
# Extraction
######

import re
import pandas as pd

# Use regex to find relevant information
invoice_number_match = re.search(r'Facture (\d+ \d+)', text)
date_match = re.search(r'(\d{2}\.\d{2}\.\d{4})', text)
amount_match = re.search(r'Total intermédiaire (\d+\.\d+)', text)
tax_match = re.search(r'TVA 2.6% net \(Code 23\) de \d+\.\d+ (\d+\.\d+)', text)

# Calculate total amount to pay
if amount_match and tax_match:
    amount_to_pay = float(amount_match.group(1)) + float(tax_match.group(1))
else:
    amount_to_pay = None

# Prepare data for the DataFrame
data = {
    'Invoice Number': [invoice_number_match.group(1) if invoice_number_match else 'N/A'],
    'Date': [date_match.group(1) if date_match else 'N/A'],
    'Amount to Pay': [amount_to_pay]
}

# Create the DataFrame
df = pd.DataFrame(data)

# Display the DataFrame
print(df)

# This works great but we want know to see if it works with invoices in different languages

#############################################
# Different Language Text Extraction
#############################################

#  'input_string' contains the invoice text
def extract_invoice_data(input_string):
    # Define patterns
    patterns = {
        'Invoice Number': r'Rechnung\s+([\d ]+)\n|Fattura\s+([\d ]+)\n|Facture\s+([\d ]+)\n',
        'Customer Number': r"Kundennummer\s+(\d{1,3}(?:'\d{3})*)|Numéro de client\s+(\d{1,3}(?:'\d{3})*)|Numero cliente\s+(\d{1,3}'?\d{3}|\d{5})",
        'Employee Name': r"Sachebearbeiter\s+(\w+)\n|Collaboratore\s+(\w+)\n|Collaborateur\s+(\w+)\n",
        'Delivery Note': r"Lieferschein\s*-\s*(\d{3}\s{1}\d{3})|Bollettino di consegna\s*-\s*(\d{3}\s{1}\d{3})\n|Bulletin de Livraison\s*-\s*(\d{3}\s{1}\d{3})",
        'Delivery Address': r'Lieferadresse \s*(.*?)\n|Adresse de fourniture \s*(.*?)\n|Indirizzo di fornitura:\s*(.*?)\n|\d+\s+-\s+(.*?,\s+\d{4}.*?)(?=\n)',
        'Date': r'(\d{2}\.\d{2}\.\d{4})|(\d{2}/\d{2}/\d{4})',
        'Subtotal': r'Total intermédiaire\s+([\d\s]+\.\d{2})|Totale intermedio\s+([\d\s]+\.\d{2})|Zwischentotal\s+([\d\s]+\.\d{2})',
        'Total': r"Total CHF\s+(\d+\.\d{2})|Totale CHF\s+(\d+\.\d{2})"
    }
    
    # Extract information
    extracted_data = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, input_string, re.IGNORECASE)
        if match:
            # Extract the first non-None group
            extracted_data[key] = next((m for m in match.groups() if m is not None), 'N/A')
        else:
            extracted_data[key] = 'N/A'
    
    return extracted_data

# Test function
extract_invoice_data(text)


#############################################
# Different Language Text Extraction
#############################################

# Prepare the DataFrame
data = {
    'Invoice Number':  [],
    'Customer Number': [],
    'Employee Name': [],
    'Delivery Note': [],
    'Delivery Address': [],
    'Subtotal': [],
    'Total': []
}

# Create the DataFrame
df_orders = pd.DataFrame(data)

# Display the DataFrame
print(df)

### Function
def add_data_to_df_orders(data, df=df_orders):        
    # Add a new row to the DataFrame with the values from the data dictionary
    df = df.append(data, ignore_index=True)
    return df


## Testing extraction and table 
## Testing function for extraction
add_data_to_df_orders(extract_invoice_data(text))