import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from .router import Router
from .handlers import home,authors,books
from app.utils.logger import create_logger
from app.utils.response import response_sender
from app.utils.read_body import read_body
from app.utils.parse_url import parse_url

logger = create_logger(name=__name__)

router = Router()

router.add("GET","/",home.home_handler)
router.add("GET","/authors",authors.authors_handler)
router.add("GET","/books",books.books_handler)

router.add("GET", "/books/<id>",books.books_handler)
router.add("GET", "/authors/<id>",authors.authors_handler)

router.add("POST","/authors",authors.create_author_handler)
router.add("POST","/books",books.create_book_handler)

router.add("DELETE","/authors/<id>",authors.delete_author_handler)
router.add("DELETE","/books/<id>",books.delete_book_handler)

router.add("PUT","/authors/<id>",authors.put_author_handler)
router.add("PUT","/books/<id>",books.put_book_handler)

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        logger.info(f"GET Request received: {self.path}")

        path, query_params = parse_url(self.path)

        handler, params = router.resolve("GET",path)

        try:
            if handler:
                status_code, response_data = handler(query_params,params)
            else:
                status_code, response_data = 404, {"error": "Not found"}
        
        except Exception as e:
            logger.error(f"Error GET: {e}")
            status_code, response_data = 500, {"error": "Internal Server Error"}

        response_sender(self,status_code,response_data)




    def do_POST(self):
        logger.info(f"POST Request received: {self.path}")
        
        path, query_params = parse_url(self.path)
            
        data = read_body(self)

        handler = router.resolve("POST",path)[0]

        try:
            if handler and (not query_params):
                status_code, response_data = handler(data)
            else:
                status_code, response_data = 404, {"error":"Not Found"}

        except Exception as e:
            logger.error(f"Error POST: {e}")
            status_code, response_data = 500, {"error": "Internal Server Error"}

        response_sender(self,status_code,response_data)




    def do_PUT(self):
        logger.info(f"PUT Request received: {self.path}")

        path, query_params = parse_url(self.path)

        data = read_body(self)

        handler, params = router.resolve("PUT",path)

        try:
            if handler:
                status_code, response_data = handler(data, params)
            else: 
                status_code, response_data = 404, {"error": "Not Found"}

        except Exception as e:
            logger.error(f"Error: {e}")
            status_code, response_data = 500, {"error": "Internal Server Error"}

        response_sender(self,status_code,response_data)

        

    def do_DELETE(self):
        logger.info(f"DELETE Request received: {self.path}")

        path, query_params = parse_url(self.path)

        handler, params = router.resolve("DELETE",path)

        try:
            if handler and (not query_params):
                status_code, response_data= handler(params)
            else:
                status_code, response_data = 404, {"error": "Not found"}

        except Exception as e:
            logger.error(f"Error: {e}")
            status_code, response_data = 500, {"error": "Internal server error"}
    
        response_sender(self,status_code, response_data)
        


def run():
    server_address = ("",8000)
    httpd = ThreadingHTTPServer(server_address,MyHandler)

    logger.info("Server Running on http://localhost:8000")

    try:
        httpd.serve_forever()

    except KeyboardInterrupt:
        logger.warning("Server stopped \"http://localhost\" no more running!! (Keyboard Interrupt)")

    finally:
        httpd.server_close()
        logger.info("Server closed cleanly")


if __name__ == "__main__":
    run()
