class Router:
    def __init__(self):
        self.routes = []

    def add(self, method, path, handler):
        self.routes.append ({
            "method": method,
            "path": path,
            "handler": handler
        })
        
    def resolve(self, method, request_path):

        for route in self.routes:

            if route["method"] != method:
                continue

            route_path = route["path"]

            if (route_path == request_path) or (route_path == request_path.rstrip("/")) :
                return route["handler"], {}
            
            route_part = route_path.strip("/").split("/")
            request_part = request_path.strip("/").split("/")

            if (len(route_part) != len(request_part)):
                continue
            
            if "<id>" in route_path:
                params = {}
                matched = True

                for rp, reqp in zip(route_part, request_part):
                    
                    if rp == "<id>":
                        if not reqp.isdigit():
                            matched = False
                            break
                        params["id"] = reqp
                        
                    elif rp != reqp:
                        matched = False

                if matched:
                    return route["handler"], params
                                
        return None, {}
            