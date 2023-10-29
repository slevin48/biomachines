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

def list_folders_and_files(bucket):
    """List folders and files in a specified S3 bucket."""
    folders = set()
    files = []
    resp = s3.list_objects_v2(Bucket=bucket)
    for obj in resp['Contents']:
        key = obj['Key']
        if '/' in key:
            folder = key.split('/')[0]
            folders.add(folder)
        files.append(key)
    return sorted(folders), files

def display_image(bucket, key):
    """Display image from S3 bucket."""
    img_bytes = s3.get_object(Bucket=bucket, Key=key)['Body'].read()
    img = Image.open(io.BytesIO(img_bytes))
    st.image(img, caption=key)

st.title('Biomachines 🧬🤖')

folders, all_files = list_folders_and_files(BUCKET_NAME)

# Sidebar for folder selection
selected_folder = st.sidebar.selectbox("Select a folder:", [""] + list(folders))

if selected_folder:
    st.write(f'Images in chapter: {selected_folder}')
    for file_key in all_files:
        if file_key.startswith(selected_folder+'/images'):
            # st.sidebar.write(file_key.replace(selected_folder+'/images/',''))
            if file_key.lower().endswith(('.png', '.jpg', '.jpeg')):
                if st.sidebar.button(f"Show {file_key.replace(selected_folder+'/images/','')}"):
                    display_image(BUCKET_NAME, file_key)
else:
    st.write("Select a folder to view its contents.")
