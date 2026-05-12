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

            if route_path == request_path:
                return route["handler"], {}
            
            if "<id>" in route_path:
                
                route_part = route_path.strip("/").split("/")
                request_part = request_path.strip("/").split("/")


                if (len(route_part) != len(request_part)):
                    continue


                params = {}
                matched = False

                if request_part[1].isdigit():
                    matched = True

                for rp, reqp in zip(route_part, request_part):
                    
                    if rp == "<id>":
                        params["id"] = reqp
                        
                    elif rp != reqp:
                        matched = False
                        break

                if matched:
                    return route["handler"], params
                
        return None, {}
            
        