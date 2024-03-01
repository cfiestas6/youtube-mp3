import streamlit as st
from pytube import YouTube
import os
import base64

def download_youtube_audio(url):
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=".")
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    return new_file

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href

st.title('YouTube Audio Downloader')

url = st.text_input('Enter the YouTube URL', '')

if st.button('Download Audio'):
    if url:
        try:
            file_path = download_youtube_audio(url)
            st.markdown(get_binary_file_downloader_html(file_path, 'MP3'), unsafe_allow_html=True)
        except Exception as e:
            st.error(f'Failed to download: {e}')
    else:
        st.error('Please enter a URL')

