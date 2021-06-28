from app.annotation_wrapper import Annotation
import requests
from app.exceptions import CredentialsException


def download_annotation(
    username: str, password: str, login_url: str, export_url: str
) -> Annotation:
    response = requests.post(
        login_url, json={"username": username, "password": password}
    )
    try:
        response.raise_for_status()
    except Exception as e:
        raise CredentialsException(response.json())

    token = response.json()["key"]

    response = requests.post(
        export_url, headers={"Authorization": "token {}".format(token)}
    )
    return Annotation(raw_str=response.content)
