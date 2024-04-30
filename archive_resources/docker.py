# from the dropdown at the top of Cloud Console:
export GCLOUD_PROJECT="ucl-engineering-invoice" 
# from Step 2.2 above:
export REPO="foo-repository"
# the region you chose in Step 2.4:
export REGION="us-east4"
# whatever you want to call this image:
export IMAGE="app.py"

# use the region you chose above here in the URL:
export IMAGE_TAG=${REGION}-docker.pkg.dev/$GCLOUD_PROJECT/$REPO/$IMAGE

# Build the image:
docker build -t $IMAGE_TAG -f /Users/alessandracerutti/ucl-invoice-assistant/text_extraction.dockerfile --platform linux/x86_64 .
# Push it to Artifact Registry:
docker push $IMAGE_TAG