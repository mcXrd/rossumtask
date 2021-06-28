from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import os

from app.download_annotation import download_annotation
from app.transform_annotation import transform_annotation
from app.send_encoded_data import send_encoded_data
from app.exceptions import PipelineException, CredentialsException

app = Flask(__name__)
app.config["ROSSUM_USER"] = os.environ.get("ROSSUM_USER")
app.config["ROSSUM_PASS"] = os.environ.get("ROSSUM_PASS")
app.config["HTTP_BASIC_USER"] = os.environ.get("HTTP_BASIC_USER", "myUser123")
app.config["HTTP_BASIC_PASS"] = os.environ.get("HTTP_BASIC_PASS", "secretSecret")
app.config["CALLBACK_URL"] = os.environ.get(
    "CALLBACK_URL", "https://my-little-endpoint.ok/rossum"
)
app.config["LOGIN_URL"] = os.environ.get(
    "LOGIN_URL", "https://api.elis.rossum.ai/v1/auth/login"
)
app.config["EXPORT_URL"] = os.environ.get(
    "EXPORT_URL",
    "https://api.elis.rossum.ai/v1/queues/{}/export?format=xml&status=exported&id={}",
)


auth = HTTPBasicAuth()

http_basic_auth_users = {
    app.config["HTTP_BASIC_USER"]: generate_password_hash(
        app.config["HTTP_BASIC_PASS"]
    ),
}


@auth.verify_password
def verify_password(username, password):
    if username in http_basic_auth_users and check_password_hash(
        http_basic_auth_users.get(username), password
    ):
        return username


@app.route("/export")
@auth.login_required
def index():
    queue_id = request.args.get("queue_id")
    annotation_id = request.args.get("annotation_id")
    if not annotation_id:
        return "annotation_id parameter is missing", 422

    if not queue_id:
        return "queue_id parameter is missing", 422

    success = True
    try:
        original_annotation = download_annotation(
            app.config["ROSSUM_USER"],
            app.config["ROSSUM_PASS"],
            app.config["LOGIN_URL"],
            app.config["EXPORT_URL"].format(queue_id, annotation_id),
        )
        transformed_annotation = transform_annotation(original_annotation)
        send_encoded_data(transformed_annotation, app.config["CALLBACK_URL"])
    except PipelineException as e:
        print(e)
        success = False
    except CredentialsException as e:
        return str(e), 401

    return {"success": success}

