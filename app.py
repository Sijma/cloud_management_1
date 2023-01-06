from flask import Flask, request
import database

app = Flask(__name__)


@app.route("/create", methods=["POST"])
def create():
    # Get the JSON payload from the request
    data = request.get_json()

    return database.register_user(data)


@app.route("/read", methods=["GET"])
def read():
    # Get the email address from the request query string
    email = request.args.get("email")

    return database.fetch_articles(email)


@app.route("/update", methods=["PUT"])
def update():
    # Get the email and new keywords from the request
    data = request.get_json()
    return database.update_keywords(data)


@app.route("/delete", methods=["DELETE"])
def delete():
    # Get the email address from the request query string
    email = request.args.get("email")

    return database.delete_user(email)


if __name__ == '__main__':
    app.run()
