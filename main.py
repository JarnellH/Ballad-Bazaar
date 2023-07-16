from flask import Flask
import requests

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(host="localhost", port=3000, debug=True)
