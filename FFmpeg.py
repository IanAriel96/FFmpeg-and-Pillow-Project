#!/usr/bin/env python3
#Author: Ian Baquero

import os
import textwrap
import subprocess
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS

# Default routes and variables
default_image_route = "./image.jpg"
default_music_route = "./music.mp3"
final_video_route = "./final_video.mp4"
voiceover_output = "voiceover.mp3"
caption = "This is a sample of caption on my video with overlay text and music"
font_route = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font_size = 50
output_image_route = "output_image.jpg"  # Imagen final

# Check if the file exists
def check_file_exists(file_path, file_type):
    if not os.path.exists(file_path):
        print(f"Error: The {file_type} file '{file_path}' is missing or cannot be found.")
        exit(1)

# Upload the image
def upload_image(image_route):
    check_file_exists(image_route, "image")
    return Image.open(image_route)

# Function to add text to the image with wrapping and centering
def add_text_to_image(image, text, rotation_angle=0):
    if rotation_angle != 0:
        image = image.rotate(rotation_angle, expand=True)

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_route, font_size)

    margin = 40
    max_width = image.width - 2 * margin
    max_height = image.height - 2 * margin

    wrapped_text = textwrap.fill(text, width=40)
    lines = [textwrap.fill(line, width=max_width // font.getbbox("A")[2]) for line in wrapped_text.split('\n')]

    total_text_height = sum(draw.textbbox((0, 0), line, font=font)[3] for line in lines)
    current_height = (image.height - total_text_height) // 2
    current_width = margin

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        position = (current_width, current_height)
        draw.text(position, line, font=font, fill="white")
        current_height += bbox[3] - bbox[1]

    return image

# Function to apply transformations (grayscale, rotation, resize)
def apply_transformation(image, transformation_type="grayscale", rotation_angle=0, resize_ratio=None):
    if transformation_type == "grayscale":
        return image.convert("L").convert("RGB")
    elif transformation_type == "rotate":
        return image.rotate(rotation_angle, expand=True)
    elif transformation_type == "resize" and resize_ratio:
        width, height = image.size
        new_size = (int(width * resize_ratio), int(height * resize_ratio))
        return image.resize(new_size)
    return image

# Function to generate voiceover using gTTS
def generate_voiceover(text, output_route):
    tts = gTTS(text=text, lang="en")
    tts.save(output_route)

# Function to generate the video with FFmpeg
def generate_video(image_route, music_route, final_video_route, voiceover_route):
    command = [
        "ffmpeg",
        "-loop", "1",
        "-framerate", "30",
        "-t", "5",
        "-i", image_route,
        "-i", music_route,
        "-i", voiceover_route,
        "-filter_complex", 
        "[0:v]format=yuv420p,scale=-2:trunc(ih/2)*2[v]; "
        "[1:a]aformat=sample_fmts=s16:sample_rates=44100:channel_layouts=stereo[a1]; "
        "[2:a]aformat=sample_fmts=s16:sample_rates=44100:channel_layouts=stereo[a2]; "
        "[a1][a2]amix=inputs=2[a]", 
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-b:a", "192k",
        "-y",
        final_video_route
    ]
    subprocess.run(command)

if __name__ == "__main__":
    image_route = input(f"Enter the image path (or press Enter to use '{default_image_route}'): ") or default_image_route
    background_music_route = input(f"Enter the background music path (or press Enter to use '{default_music_route}'): ") or default_music_route

    check_file_exists(image_route, "image")
    check_file_exists(background_music_route, "background music")

    image = upload_image(image_route)

    valid_transformations = {"grayscale", "rotate", "resize", ""}
    transformation = ""

    while True:
        transformation = input("Enter the transformation you want (grayscale, rotate, resize) or press Enter to skip: ").strip().lower()
        if transformation in valid_transformations:
            break
        print("Invalid input.")

    if transformation == "resize":
        resize_ratio = float(input("Enter the resize ratio (ex. 0.5 for 50% size, 2 for double size): "))
        image = apply_transformation(image, transformation, resize_ratio=resize_ratio)
    elif transformation == "rotate":
        rotation_angle = float(input("Enter the rotation angle in degrees (ex. 90, 180, etc.): "))
        image = apply_transformation(image, transformation, rotation_angle=rotation_angle)
    elif transformation == "grayscale":
        image = apply_transformation(image, transformation)

    overlay_text = input("Enter the text you want to overlay on the image: ")
    image = add_text_to_image(image, overlay_text)

    image.save(output_image_route)
    print(f"Image saved as '{output_image_route}'")

    generate_voiceover(caption, voiceover_output)
    generate_video(output_image_route, background_music_route, final_video_route, voiceover_output)

    print(f"Video successfully generated at {final_video_route}")
