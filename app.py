from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    a = 5
    b = 7
    result = a + b
    return f"""
        <h1>Hello from Jenkins CI/CD pipeline test!</h1>
        <h2>Addition Result:</h2>
        <p>{a} + {b} = {result}</p>
    """

if __name__ == '__main__':
    print("This message will show in terminal logs")
    app.run(host='0.0.0.0', port=5000)
