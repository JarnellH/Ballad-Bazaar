from flask import Flask, request
import openai
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/test_get', methods=['GET'])
def test_get():
    return { "message": "hello there" }

@app.route('/analyze_lyrics', methods=['POST'])
def analyze_lyrics():
    data = request.get_json()
    lyrics = data.get("lyrics")

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"""
        Take the given song lyrics and analyze them to derive the main themes and emotions. 
        Using this analysis, create four distinctive prompts that could be used to inspire scenes in a music video.
        Lyrics: {lyrics}
        """,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return {"prompts": response.choices[0].text.strip()}

if __name__ == '__main__':
    app.run(host="localhost", port=3000, debug=True)