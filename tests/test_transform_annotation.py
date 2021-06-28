from app.transform_annotation import transform_annotation
from app.annotation_wrapper import Annotation
from pathlib import Path
from unittest import TestCase

original_path = Path(__file__).with_name("original.xml")
with original_path.open("r") as f:
    ORIGINAL_MOCK = f.read()

transformed_path = Path(__file__).with_name("transformed.xml")
with transformed_path.open("r") as f:
    TRANSFORMED_MOCK = f.read()


def test_transform_annotation():
    original_annotation = Annotation(raw_str=ORIGINAL_MOCK)
    transformed_annotation = transform_annotation(original_annotation)
    tc = TestCase()
    tc.maxDiff = None
    tc.assertDictEqual(
        Annotation(raw_str=TRANSFORMED_MOCK).dict_repr,
        transformed_annotation.dict_repr,
    )
