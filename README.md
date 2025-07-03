# Video Generator by Frame

A simple CLI tool to generate a video from a sequence of images (from a folder or a ZIP file). Built with Python and ffmpeg.

## Features
- Combine images from a folder or ZIP into a video
- Choose video FPS or total duration
- Supports PNG, JPG, JPEG, BMP, TIFF
- Output in MP4 (H.264)

## Requirements
- Python 3.8+
- ffmpeg (must be installed and available in your PATH)
- Python packages: ffmpeg-python

## Installation

1. **Clone or download this repository**

2. **Install Python dependencies**

```sh
pip install ffmpeg-python
```

3. **Install ffmpeg**
- Download from https://ffmpeg.org/download.html
- Add ffmpeg to your system PATH (so you can run `ffmpeg` from the command line)

## Usage

Run the CLI tool:

```sh
python main.py
```

Follow the prompts:
- Choose FPS or total duration
- Choose images from a folder or ZIP file
- Enter the required paths

The output video will be saved as `output.mp4` in the current directory.

## Example

```
$ python main.py
How do you want to configure the video?
1. By frames per second (FPS)
2. By total duration
Enter your choice (1 or 2):
...
```

## Notes
- Images should be named so that sorting them alphabetically gives the wished order.
- ZIP files cant contain the images in subfolders.
