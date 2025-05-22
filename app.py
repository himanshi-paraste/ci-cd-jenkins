from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    a = 5
    b = 7
    result = a + b
    return f"<h1>Addition Result:</h1><p>{a} + {b} = {result}</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
