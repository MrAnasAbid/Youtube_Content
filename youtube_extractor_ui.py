import os
import cv2
import numpy as np
import streamlit as st
from pytube import YouTube
from sklearn.metrics import mean_squared_error

# Function to download video from YouTube
def download_video(url, output_path='video.mp4'):
    st.write(f'Downloading video from {url}...')
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
    stream.download(filename=output_path)
    st.write('Video downloaded successfully!')

# Function to extract frames from the video
def extract_frames(video_path, frame_rate=1):
    st.write(f'Extracting frames from {video_path}...')
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps / frame_rate)
    
    frames = []
    for i in range(0, frame_count, frame_interval):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if ret:
            frames.append(frame)
    
    cap.release()
    return frames

# Function to determine if a frame is unique based on Mean Squared Error (MSE)
def is_unique_frame(frame1, frame2, threshold=30):
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    mse = mean_squared_error(gray1.flatten(), gray2.flatten())
    return mse > threshold

# Function to extract unique slides from frames
def extract_unique_slides(frames):
    st.write('Extracting unique slides from all frames...')
    unique_slides = []
    prev_frame = None
    
    for frame in frames:
        if prev_frame is None or is_unique_frame(prev_frame, frame):
            unique_slides.append(frame)
            prev_frame = frame
    
    return unique_slides

# Function to save slides to a specified folder
def save_slides(slides, output_folder='slides'):
    if not os.path.exists(output_folder):
        st.write(f'Creating folder {output_folder} to save slides...')
        os.makedirs(output_folder)
    else:
        st.write(f'Folder {output_folder} already exists. Saving slides...')
    
    for i, slide in enumerate(slides):
        st.write(f'Saving slide {i+1}...')
        slide_path = os.path.join(output_folder, f'slide_{i+1}.png')
        cv2.imwrite(slide_path, slide)
    
    st.write('Slides saved successfully!')

# Streamlit UI code
def main():
    st.title('YouTube Slide Extractor')
    st.markdown('### Enter YouTube Video URL:')
    video_url = st.text_input('URL')
    frame_rate = st.slider('Select frame rate to extract frames:', min_value=1, max_value=10, value=1)
    output_folder = st.text_input('Enter output folder name:', value='slides')

    if st.button('Extract Slides'):
        if video_url:
            st.write('Processing...')
            video_path = 'video.mp4'
            download_video(video_url, video_path)
            frames = extract_frames(video_path, frame_rate)
            unique_slides = extract_unique_slides(frames)
            save_slides(unique_slides, output_folder)
            st.success('Slides extraction and saving completed!')
        else:
            st.warning('Please enter a YouTube video URL.')

if __name__ == '__main__':
    main()
