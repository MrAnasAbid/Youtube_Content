# YouTubeHighlighter 
*YouTubeHighlighter* is a project designed to extract unique slides from a YouTube video. It efficiently downloads the video, captures frames at a specified rate, identifies unique slides based on image similarity, and saves them in a designated folder. This tool is perfect if:

* You don't want to sit through a whole 30-minute video that contains only 2 easy-to-understand slides.
* You want quick information from multiple videos at once.
* You have a deadline and need to understand your professor's course quickly (because you procrastinated).

## Features

* Unique Slide Detection: Identifies and saves only distinct slides, avoiding redundant frames.
* Customizable Frame Rate: Control the video frame extraction rate to optimize processing speed and image quality.
* Flexible Output Folder: Specify the folder location to save the extracted slides.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/youtube-slide-extractor.git
cd youtube-slide-extractor
```

2. Install dependencies:

* Using pip:
```bash
pip install -r requirements.txt
```

* Using pipenv (recommended):
```bash
pipenv install
```

## Usage

Run the YouTube Slide Extractor with the following command:

```bash
python slide_extractor.py "https://www.youtube.com/sample_url" --frame_rate 1 --output_folder "slides"
```

* Replace "https://www.youtube.com/sample_url" with the desired YouTube video URL.
* Adjust --frame_rate (default: 1 frame per second) to control the extraction rate between frames. A higher rate captures more slides but takes longer.
* Adjust --output_folder (default: "slides") to specify the folder where the extracted slides will be saved.

## Improvements

* This project is still in progress. The main areas of improvement include more efficient filtering of redundant slides and developing a more robust packaging software around it.
