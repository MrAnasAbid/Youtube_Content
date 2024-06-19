import os
import cv2
import numpy as np
from pytube import YouTube
from sklearn.metrics import mean_squared_error

# Step 1: Download the video
def download_video(url, output_path='video.mp4'):
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
    stream.download(filename=output_path)

# Step 2: Extract frames from the video
def extract_frames(video_path, frame_rate=1):
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

# Step 3: Identify unique slides by comparing consecutive frames
def is_unique_frame(frame1, frame2, threshold=30):
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    mse = mean_squared_error(gray1.flatten(), gray2.flatten())
    return mse > threshold

def extract_unique_slides(frames):
    unique_slides = []
    prev_frame = None
    
    for frame in frames:
        if prev_frame is None or is_unique_frame(prev_frame, frame):
            unique_slides.append(frame)
            prev_frame = frame
    
    return unique_slides

# Step 4: Save the unique slides to a folder
def save_slides(slides, output_folder='slides'):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for i, slide in enumerate(slides):
        slide_path = os.path.join(output_folder, f'slide_{i+1}.png')
        cv2.imwrite(slide_path, slide)

# Main function to process the video and extract slides
def main(url):
    video_path = 'video.mp4'
    download_video(url, video_path)
    
    frames = extract_frames(video_path, frame_rate=1)  # Adjust frame_rate as needed
    unique_slides = extract_unique_slides(frames)
    save_slides(unique_slides)

# Run the main function with the provided YouTube URL
if __name__ == '__main__':
    video_url = 'https://www.youtube.com/watch?v=Bqoz7b7nFyk'
    main(video_url)
