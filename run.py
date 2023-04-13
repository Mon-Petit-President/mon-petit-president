from flask import Flask, render_template
import os

app = Flask(__name__)


@app.route('/')
def index():
    return 'Index Page de MPP'

@app.route('/hello')
def hello():
    return 'Hello MPP'

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
