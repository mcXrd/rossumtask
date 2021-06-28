import requests_mock
from app.send_encoded_data import send_encoded_data
from pathlib import Path
from app.annotation_wrapper import Annotation
import pytest
from app.exceptions import PipelineException

transformed_path = Path(__file__).with_name("transformed.xml")
with transformed_path.open("r") as f:
    TRANSFORMED_MOCK = f.read()


def test_send_encoded_data_ok():
    with requests_mock.Mocker() as mock:
        url = "https://my-little-endpoint.ok/rossum"
        mock.post(url, json={"status": "ok"})
        send_encoded_data(Annotation(raw_str=TRANSFORMED_MOCK), url, 123456)


def test_send_encoded_data_nok():
    with requests_mock.Mocker() as mock:
        url = "https://my-little-endpoint.ok/rossum"
        mock.post(url, json={"status": "fail"}, status_code=400)
        with pytest.raises(PipelineException) as e:
            send_encoded_data(Annotation(raw_str=TRANSFORMED_MOCK), url, 123456)
