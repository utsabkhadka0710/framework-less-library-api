import json


def response_sender(self, status_code=404, response_data=None):

    if not response_data:
        response_data = {"error": "Not found"}

    self.send_response(status_code)
    self.send_header("Content-Type","application/json")
    self.end_headers()
    self.wfile.write(json.dumps(response_data, indent=4).encode())