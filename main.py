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

@app.route('/result')
def result():
    return app.send_static_file('result.html')

@app.route('/begin_video_generation', methods=['POST'])
def begin_video_generation():
    lyrics = request.form.get("lyrics")
    print(lyrics)
    if 'song' not in request.files:
        return {'message': 'No mp3 file in request'}
    song = request.files['song']
    if song.filename == '':
        return {'message': 'No selected file'}
    if song:
        filename = secure_filename(song.filename)
        song.save(os.path.join('', filename))
        return {"done": 'donnne'}

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

# overlays the given video clip with the audio clip, use when final video is made
def overlayAudio(clip, audio):
    clipLen = clip.duration
    audLen = audio.duration
    if clipLen < audLen:
        cuttoff = clipLen-audLen
        audio = audio.subclip(0, cuttoff)
    elif  clipLen > audLen:
        cuttoff = audLen-clipLen
        clip = clip.subclip(0,cuttoff)
    clip.audio = audio
    clip.write_videofile("NewMusicVideo.mp4")
    clip.close()

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
#@app.route('/transition')
def transition(path1, path2, name):
    firstVid = path1
    secondVid = path2
    firstVid1Frame, firstVid2Frame = extract_frames(firstVid)
    lastVid1Frame, lastVid2Frame = extract_frames(secondVid)
    frameRate = 10
    im_arr = []
    firstOpacity = 1.0
    secondOpacity = 0
    height, width, layers = firstVid1Frame.shape
    size = (width, height)
    increment = 1.0/frameRate
    for i in range(0,frameRate):
        blended = cv2.addWeighted(firstVid2Frame, firstOpacity, lastVid1Frame, secondOpacity, 0 )
        im_arr.append(blended)
        #cv2.imshow('image',blended)
        firstOpacity -= increment
        secondOpacity += increment

    out = cv2.VideoWriter('secondProject.mp4',0x7634706d, 30, size )
    print(out)
    middleVid = "C:\\Users\\Erics\\Ballad-Bazaar\\secondProject.mp4"
    print(len(im_arr))
    for i in range(0, len(im_arr)):
        #cv2.imshow("Frame", im_arr[i])
        #cv2.waitKey(0)
        out.write(im_arr[i])

    out.release()
    clip1 = VideoFileClip(firstVid)
    clip2 = VideoFileClip(middleVid)
    clip3 = VideoFileClip(secondVid)
    final_clip = concatenate_videoclips([clip1,clip2,clip3])
    final_clip.write_videofile(name)
    
    return name 

#use this one
@app.route('/videomaker')
def videoMaker():
    vid1 = "video1"
    prompt = "A wealthy man, once accustomed to a life of privilege, finds himself humbled and on his knees, pleading for help or forgiveness from those around him."
    response = requests.get(f'https://thomaspinella--my-app-fastapi-app-dev.modal.run/vid?name={vid1}&prompt={prompt}')
    print("first one done")
    file_path1 = 'C:\\Users\\Erics\\Ballad-Bazaar\\static\\video1.mp4'
    with open(file_path1, 'wb') as file:
        file.write(response.content)

    vid2 = "video2"
    prompt2 = "A morally upright man, known for his integrity, succumbs to temptation and commits a sinful act, struggling with the consequences and wrestling with guilt."
    response2 = requests.get(f'https://thomaspinella--my-app-fastapi-app-dev.modal.run/vid?prompt={prompt2}&name={vid2}')
    print("second one done")
    file_path2 = 'C:\\Users\\Erics\\Ballad-Bazaar\\static\\video2.mp4'
    with open(file_path2, 'wb') as file:
        file.write(response2.content)

    vid3 = "video3"
    prompt3 = "A strong and resilient man, typically seen as tough and unyielding, breaks down emotionally, shedding tears that reveal his vulnerability and inner turmoil."
    response3 = requests.get(f'https://thomaspinella--my-app-fastapi-app-dev.modal.run/vid?name={vid3}&prompt={prompt3}')
    print("third one done")
    file_path3 = 'C:\\Users\\Erics\\Ballad-Bazaar\\static\\video3.mp4'
    with open(file_path3, 'wb') as file:
        file.write(response3.content)

    vid4 = "video4"
    prompt4 = "A person considered a loser or underdog achieves a surprising victory, overcoming obstacles and defying expectations, resulting in a triumphant and joyful moment of celebration."
    response4 = requests.get(f'https://thomaspinella--my-app-fastapi-app-dev.modal.run/vid?name={vid4}&prompt={prompt4}')
    print("fourth one done")
    file_path4 = 'C:\\Users\\Erics\\Ballad-Bazaar\\static\\video4.mp4'
    with open(file_path4, 'wb') as file:
        file.write(response4.content)

    combinePath1 = 'C:\\Users\\Erics\\Ballad-Bazaar\\static\\video5.mp4'
    combinePath2 = 'C:\\Users\\Erics\\Ballad-Bazaar\\static\\video6.mp4'
    combinePath3 = 'C:\\Users\\Erics\\Ballad-Bazaar\\static\\video7.mp4'
    #firstVid = "C:\\Users\\Erics\\Ballad-Bazaar\\static\\our-video (1).mp4"
    #secondVid = "C:\\Users\\Erics\\Ballad-Bazaar\\static\\our-video (1).mp4"
    firstVid = file_path1
    secondVid = file_path2
    thirdVid = file_path3
    fourthVid = file_path4
    firstCombine = VideoFileClip(transition(firstVid,secondVid,combinePath1))
    #firstAddress  = os.path.abspath(firstCombine)
    secondCombine = VideoFileClip(transition(combinePath1,thirdVid,combinePath2))
    #secondAddress  = os.path.abspath(secondCombine)
    final_clip = VideoFileClip(transition(combinePath2,fourthVid,combinePath3))

    audio_background = AudioFileClip("C:\\Users\\Erics\\Ballad-Bazaar\\Everlas.mp3")
    overlayAudio(final_clip, audio_background )
    return {"message: working"}

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
        #cv2.imshow('image',blended)
        firstOpacity -= increment
        secondOpacity += increment

    out = cv2.VideoWriter('project.mp4',0x7634706d, 15, size )
    print(len(im_arr))
    for i in range(0, len(im_arr)):
        #cv2.imshow("Frame", im_arr[i])
        #cv2.waitKey(0)
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




if __name__ == '__main__':
    app.run(host="localhost", port=3000, debug=True)
