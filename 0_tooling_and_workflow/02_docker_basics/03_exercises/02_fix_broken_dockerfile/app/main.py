from flask import Flask

app = Flask(__name__)


@app.route("/")
def index() -> str:
    return "hello from broken-dockerfile exercise\n"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
