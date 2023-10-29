import streamlit as st
import boto3
from PIL import Image
import io

# AWS S3 Configuration
AWS_ACCESS_KEY_ID = st.secrets['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = st.secrets['AWS_SECRET_ACCESS_KEY']
BUCKET_NAME = "biomachines"

# Initialize a session using an AWS profile
session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


# Initialize S3 client
s3 = session.client('s3')

def list_files(bucket):
    """List files in a specified S3 bucket."""
    files = []
    resp = s3.list_objects_v2(Bucket=bucket)
    for obj in resp['Contents']:
        files.append(obj['Key'])
    return files

def display_image(bucket, key):
    """Display image from S3 bucket."""
    img_bytes = s3.get_object(Bucket=bucket, Key=key)['Body'].read()
    img = Image.open(io.BytesIO(img_bytes))
    st.image(img, caption=key)

st.title('S3 Bucket Explorer')

files = list_files(BUCKET_NAME)
st.write('Files and folders in the bucket:')
for file_key in files:
    st.sidebar.write(file_key)
    if file_key.lower().endswith(('.png', '.jpg', '.jpeg')):
        if st.button(f"Show {file_key}"):
            display_image(BUCKET_NAME, file_key)
