from app.annotation_wrapper import Annotation
import requests
import base64
from app.exceptions import PipelineException


def send_encoded_data(
    transformed_annotation: Annotation, callback_url: str, annotation_id: int
):
    base64_content = base64.b64encode(transformed_annotation.raw_str.encode("ascii"))
    response = requests.post(
        callback_url,
        json={"annotationId": annotation_id, "content": str(base64_content)},
    )
    try:
        response.raise_for_status()
    except Exception as e:
        raise PipelineException(str(e))
