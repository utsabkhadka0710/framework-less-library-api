import json

def read_body(handler):
    content_length = int(handler.headers.get("Content-Length",0))
    body = handler.rfile.read(content_length)
    try:
        return json.loads(body)
    except:
        return {}
