import os
import cv2
import numpy as np
import click
from pytube import YouTube
from sklearn.metrics import mean_squared_error

def download_video(url, output_path='video.mp4'):
    print(f'Downloading video from {url}...')
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
    stream.download(filename=output_path)
    print('Video downloaded successfully!')

def extract_frames(video_path, frame_rate=1):
    print(f'Extracting frames from {video_path}...')
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

def is_unique_frame(frame1, frame2, threshold=30):
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    mse = mean_squared_error(gray1.flatten(), gray2.flatten())
    return mse > threshold

def extract_unique_slides(frames):
    print('Extracting unique slides from all the frames...')
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
        print(f'Creating folder {output_folder} to save slides...')
        os.makedirs(output_folder)
    else:
        print(f'Folder {output_folder} already exists. Saving slides...')
    
    for i, slide in enumerate(slides):
        print(f'Saving slide {i+1}...')
        slide_path = os.path.join(output_folder, f'slide_{i+1}.png')
        cv2.imwrite(slide_path, slide)
    
    print('Slides saved successfully!')

# Main function to process the video and extract slides
@click.command()
@click.argument('url')
@click.option('--frame_rate', default=1, help='Frame rate to extract frames from the video.')
@click.option('--output_folder', default='slides', help='Folder to save the extracted slides.')
def main(url, frame_rate, output_folder):
    video_path = 'video.mp4'
    download_video(url, video_path)
    
    frames = extract_frames(video_path, frame_rate)  # Adjust frame_rate as needed
    unique_slides = extract_unique_slides(frames)
    save_slides(unique_slides, output_folder)

if __name__ == '__main__':
    main()