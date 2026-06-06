import json
from json import JSONDecodeError
from .logger import create_logger

logger = create_logger(__name__)
def read_body(handler):
    content_length = int(handler.headers.get("Content-Length",0))

    if content_length == 0:
        return {}

    body = handler.rfile.read(content_length)
    try:
        return json.loads(body)
    except JSONDecodeError as e:
        logger.error(f"[MALFORMED JSON] Failed to parse requst boody: {e}")
        return {}
    except Exception as e:
        logger.error(f"[SERVER ERROR] Failed to parse requst boody: {e}")

