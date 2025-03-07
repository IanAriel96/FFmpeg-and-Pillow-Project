# FFmpeg and Pillow Project
## Objective 
A python script that generates a short video from an image using FFmpeg and Pillow. The script overlays text onto the image, apply a basic transformation (e.g., grayscale or rotation), and then convert it into a short video clip with background music and captions with a narrator

## Features
- Supports image transformations: **grayscale, rotate, or resize**
- Adds overlay text to the image
- Generates voiceover using **Google Text-to-Speech (gTTS)**
- Combines image, background music, and voiceover into a video using **FFmpeg**

## Requirements
- Python 3.x
- Required Python libraries:
  - `PIL` 
  - `gtts`
  - `textwrap`
  - `subprocess`
- **FFmpeg** installed on your system

## Installation
1. Install dependencies for linux:
   ```
   pip install pillow gtts
   ```
   ```
   sudo apt install ffmpeg  
   ```

## Usage
1. Place your image (`image.jpg`) and background music (`music.mp3`) in the project directory.
2. Run the script:
   ```
   python script.py
   ```
3. Follow the prompts to:
   - Provide image and music paths (or press Enter to use default values)
   - Select an image transformation (or skip by pressing Enter)
   - Add overlay text
   - Automatically generate the video

## Output
- The final video is saved as `final_video.mp4`.
- The processed image with text overlay is saved as `output_image.jpg`.
- The generated voiceover is stored as `voiceover.mp3`.






