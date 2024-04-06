###############################################################################
#### Invoice Scanner ####
###############################################################################

### Imports
import os
import io
import pandas as pd
from google.cloud import storage #!pip install google-cloud-storage


#from template_specification_gcp_postgres import project_id, region, instance_name, current_user, DB_USER, DB_PASS, DB_NAME

#### CONNECTING TO GCP ENVIRONMENT ####
# 1. Ensure your secrets are in json file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "your_secrets_for_gcp.json"



###############################################################################
#### CREATE BUCKET  ####
###############################################################################

# Buckets will be needed to upload the scan of the invoices and bank statements

# Instantiates a client
storage_client = storage.Client()

## Invoice BUCKET ##
bucket_name = "invoice_scan"
bucket = storage_client.create_bucket(bucket_name)
print(f"Bucket {bucket.name} created.")

## Bank Statement BUCKET ##
bucket_name = "bank_statement_scan"
bucket = storage_client.create_bucket(bucket_name)
print(f"Bucket {bucket.name} created.")


###############################################################################
#### WRITE ON THE BUCKET ####
###############################################################################

# Upload image data to ucl-forest bucket

# define function to upload different folders of the images
def upload_directory_to_bucket(bucket_name, source_directory):
    """Uploads a directory to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    
    for local_dir, _, files in os.walk(source_directory):
        for file in files:
            local_file_path = os.path.join(local_dir, file)
            
            # Construct the full path for the destination blob
            # Using the folder names as the blob prefix
            relative_path = os.path.relpath(local_file_path, source_directory)
            destination_blob_name = relative_path.replace("\\", "/")  # Ensure proper path format for GCS
            
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(local_file_path)
            
            print(f'File {local_file_path} uploaded to {destination_blob_name}.')

# upload bank statements on the bucket
upload_directory_to_bucket('bank_statement_scan', 'data/bank_statement_scan')

# upload invoice statements on the respective bucket
upload_directory_to_bucket('invoice_scan', 'data/invoice_scan')



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

pdf_file = '/Users/alessandracerutti/ucl-invoice-assistant/data/invoice_scan/invoice_10.pdf'
text = get_text_from_any_pdf(pdf_file)
