from flask import Flask, request
import database

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route("/Create", methods=["POST"])
def create():
    # Get the JSON payload from the request
    data = request.get_json()

    return database.register_user(data)


@app.route("/Read", methods=["GET"])
def read():
    # Get the email address from the request query string
    email = request.args.get("email")

    return database.fetch_articles(email)


if __name__ == '__main__':
    app.run()
