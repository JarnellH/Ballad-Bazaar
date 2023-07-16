from flask import Flask, render_template, flash, request, redirect, url_for
import openai
import re  # Add this line
from dotenv import load_dotenv
from moviepy.editor import *
import cv2
import os
from werkzeug.utils import secure_filename

import requests


app = Flask(__name__)
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

prompt_storage = []

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/generate_music_video', methods=['POST'])
def generate_music_video():
    prompt = "Purple Dinosaur Dancing in a cave"
    response = requests.get(f'https://thomaspinella--my-app-fastapi-app-dev.modal.run/vid?prompt={prompt}')
    # with open('video.mp4', 'wb') as f:
    #     f.write(response.content)
    return response

@app.route('/test_get', methods=['GET'])
def test_get():
    return { "message": "hello there" }

<<<<<<< HEAD
@app.route('/analyze_lyrics', methods=['POST'])
def analyze_lyrics():
    global prompt_storage 
    data = request.get_json()
    lyrics = data.get("lyrics")

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"""
        Take the given song lyrics and analyze them.
        Using this analysis, generate four distinctive prompts that could be used to inspire scenes in a music video.
        Please format each response as one sentence, and separate each response with a period.
        Lyrics: {lyrics}
        """,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    prompts = response.choices[0].text.strip().split('.') # Separate prompts by period
    prompts = [prompt.strip() for prompt in prompts if prompt]

    for prompt in prompts:
        prompt_storage.append(prompt)

    return {"prompts": prompts}

@app.route('/get_prompts', methods=['GET'])  # Get stored prompts
def get_prompts():
    return {"stored_prompts": prompt_storage}

if __name__ == '__main__':
    app.run(host="localhost", port=3000, debug=True)
=======
@app.route("/hello")
def hello():
    return "Hello, Welcome to GeeksForGeeks"

def extract_frames(video_path):
    # Open the video file
    video = cv2.VideoCapture(video_path)
    
    # Get total number of frames in the video
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Grab the first frame
    video.set(cv2.CAP_PROP_POS_FRAMES, 0)
    ret, first_frame = video.read()
    
    # Grab the last frame
    video.set(cv2.CAP_PROP_POS_FRAMES, total_frames - 1)
    ret, last_frame = video.read()
    
    # Release the video file
    video.release()
    
    return first_frame, last_frame

@app.route('transition')
def transition(firstVid, secondVid):
    first_frame, last_frame = extract_frames(firstVid)
    first_frame, last_frame = extract_frames(secondVid)


@app.route('/img')
def imgDisplay():
    # Path to the MP4 video file
    video_path = "C:\\Users\\Erics\\Ballad-Bazaar\\static\\WIN_20230715_15_59_03_Pro.mp4"

    # Call the function to extract frames
    first_frame, last_frame = extract_frames(video_path)

    # Display the first frame
    #cv2.imshow("First Frame", first_frame)
    #cv2.waitKey(0)
    #return render_template("img.html", user_image = first_frame)
    # Display the last frame
    #cv2.imshow("Last Frame", last_frame)
    #cv2.waitKey(0)
    frameRate = 20
    im_arr = []
    firstOpacity = 1.0
    secondOpacity = 0
    height, width, layers = first_frame.shape
    size = (width, height)
    increment = 1.0/frameRate
    for i in range(0,frameRate):
        blended = cv2.addWeighted(first_frame, firstOpacity, last_frame, secondOpacity, 0 )
        im_arr.append(blended)
        cv2.imshow('image',blended)
        firstOpacity -= increment
        secondOpacity += increment

    out = cv2.VideoWriter('project.mp4',0x7634706d, 15, size )
    print(len(im_arr))
    for i in range(0, len(im_arr)):
        cv2.imshow("Frame", im_arr[i])
        cv2.waitKey(0)
        out.write(im_arr[i])
        
    #media.save(video, name=filename)
    #out.save(os.path.join("/tmp/", "myFile"))
    out.release()
    # Close all windows
    cv2.destroyAllWindows()
    #return app.send_static_file('img.html')
    return render_template('img.html')

if __name__ == '__main__':
    app.run(host="localhost", port=3000, debug=True)


# overlays the given video clip with the audio clip, use when final video is made
def overlayAudio(clip, audio):
    clip.audio = audio
    clip.write_videofile("NewMusicVideo.mp4")
    clip.close()



>>>>>>> main
