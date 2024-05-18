import json


def load_request_body(body):
    if isinstance(body, str):
        try:
            body: dict = json.loads(body)
            return body
        except json.JSONDecodeError:
            return body
    return body
