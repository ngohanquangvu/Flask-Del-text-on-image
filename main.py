from flask import Flask, request, send_file
app = Flask(__name__)

@app.route('/hello/')
def hello():
    return "hello"
if __name__ == '__main__':
    app.run(debug=True)
