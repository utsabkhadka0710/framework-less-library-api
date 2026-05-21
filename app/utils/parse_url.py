from urllib.parse import urlparse, parse_qs


def parse_url(handler_path):

    parsed = urlparse(handler_path)
    path = parsed.path
    query_params = parse_qs(parsed.query)
    
    return path, query_params
