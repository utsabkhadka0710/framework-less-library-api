import json


def response_sender(handler, status_code=404, response_data=None):

    if not response_data:
        response_data = {"error": "Not found"}

    handler.send_response(status_code)
    handler.send_header("Content-Type","application/json")
    handler.end_headers()
    handler.wfile.write(json.dumps(response_data, indent=4).encode())