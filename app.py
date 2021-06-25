from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config["ROSSUMUSER"] = os.environ.get("ROSSUMUSER")
app.config["ROSSUMPASS"] = os.environ.get("ROSSUMPASS")

auth = HTTPBasicAuth()

http_basic_auth_users = {
    app.config["ROSSUMUSER"]: generate_password_hash(app.config["ROSSUMPASS"]),
}


@auth.verify_password
def verify_password(username, password):
    if username in http_basic_auth_users and check_password_hash(
        http_basic_auth_users.get(username), password
    ):
        return username


@app.route("/")
@auth.login_required
def index():
    annotation_id = request.args.get("annotation_id")

    return "Hello World! {} --- {}".format(app.config.get("EVV"), annotation_id)
