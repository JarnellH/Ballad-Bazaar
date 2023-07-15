from flask import Flask

app = Flask(__name__)

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/test_get', methods=['GET'])
def test_get():
    return { "message": "hello there" }

if __name__ == '__main__':
    app.run(host="localhost", port=3000, debug=True)
