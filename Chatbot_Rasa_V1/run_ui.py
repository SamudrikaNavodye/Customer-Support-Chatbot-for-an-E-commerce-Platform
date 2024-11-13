from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/')
def serve_ui():
    return send_from_directory('', 'chatbot_ui.html')

if __name__ == '__main__':
    app.run(port=5500)
