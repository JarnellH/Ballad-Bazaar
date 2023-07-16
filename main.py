from flask import Flask, request
import openai
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

prompt_storage = []

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/test_get', methods=['GET'])
def test_get():
    return { "message": "hello there" }

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
        Lyrics: {lyrics}
        """,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    prompts = re.split('1\.|2\.|3\.|4\.', response.choices[0].text.strip()) # Separate prompts by numbers
    prompts = [prompt.strip() for prompt in prompts if prompt]

    for prompt in prompts:
        prompt_storage.append(prompt)

    return {"prompts": prompts}

@app.route('/get_prompts', methods=['GET'])  # Get stored prompts
def get_prompts():
    return {"stored_prompts": prompt_storage}

if __name__ == '__main__':
    app.run(host="localhost", port=3000, debug=True)