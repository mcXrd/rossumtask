from app.download_annotation import download_annotation
import requests_mock
from pathlib import Path
from unittest import TestCase
from app.annotation_wrapper import Annotation

original_path = Path(__file__).with_name("original.xml")
with original_path.open("r") as f:
    ORIGINAL_MOCK = f.read()


def test_download_annotation():
    with requests_mock.Mocker() as mock:
        mock.post(
            "https://api.elis.rossum.ai/v1/auth/login", json={"key": "asdfsfdsdfsdf"}
        )
        mock.post(
            "https://api.elis.rossum.ai/v1/queues/8236/export?format=xml&status=exported&id=123456",
            content=ORIGINAL_MOCK.encode("ascii"),
        )
        annotation = download_annotation(
            "myUser123",
            "secretSecret",
            "https://api.elis.rossum.ai/v1/auth/login",
            "https://api.elis.rossum.ai/v1/queues/8236/export?format=xml&status=exported&id=123456",
        )
        tc = TestCase()
        tc.maxDiff = None
        tc.assertDictEqual(
            Annotation(raw_str=ORIGINAL_MOCK).dict_repr,
            annotation.dict_repr,
        )
