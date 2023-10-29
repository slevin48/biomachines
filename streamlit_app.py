import streamlit as st
import boto3, io, tempfile
from PIL import Image

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

def download_and_display_video(bucket, key):
    """Download and display video from S3 bucket."""
    video_bytes = s3.get_object(Bucket=bucket, Key=key)['Body'].read()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmpfile:
        tmpfile.write(video_bytes)
        st.video(tmpfile.name)

st.title('Biomachines 🧬🤖')

folders, all_files = list_folders_and_files(BUCKET_NAME)

# Sidebar for folder selection
selected_folder = st.sidebar.selectbox("Select a chapter:", [""] + list(folders))

if selected_folder:
    st.write(f'Chapter: {selected_folder}')
    video_key = f"{selected_folder}/{selected_folder}_9x16.mp4"
    if video_key in all_files:
        if st.button(f"Show Video"):
            download_and_display_video(BUCKET_NAME, video_key)
    # for file_key in all_files:
    #     if file_key.startswith(selected_folder):
    #         st.write(file_key)
    for file_key in all_files:
        if file_key.startswith(selected_folder+'/images'):
            # st.sidebar.write(file_key.replace(selected_folder+'/images/',''))
            if file_key.lower().endswith(('.png', '.jpg', '.jpeg')):
                if st.sidebar.button(f"Show {file_key.replace(selected_folder+'/images/','')}"):
                    display_image(BUCKET_NAME, file_key)
else:
    st.write("Select a chapter to view its contents.")
