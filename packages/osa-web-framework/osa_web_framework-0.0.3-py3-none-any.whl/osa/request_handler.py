# request_handler.py

from webob import Response
from http import HTTPStatus
from osa.exceptions import HTTPException
from osa.error_handlers import debug_exception_handler 
import inspect
from .router import Router

class RequestHandler:
    def __init__(self,debug=True):
        self._routes = {}
        self.exception_handlers =  {}
        self.middleware = []
        self.debug = debug

    def add_middleware(self, middleware):
        self.middleware.append(middleware)

    def find_route(self, path):
        for pattern, route in self._routes.items():
            route , kwargs = route.match(path)
            if route is not None:
                return route , kwargs
        raise HTTPException(HTTPStatus.NOT_FOUND)
    
    def get_handler(self, route, request_method):
        ''' Get the handler function for the route and request method '''
        if inspect.isclass(route.handler):
            handler_instance = route.handler()
            handler_function = getattr(handler_instance, request_method.lower(), None)
            if handler_function is None:
                raise HTTPException(HTTPStatus.METHOD_NOT_ALLOWED)
            else:
                return handler_function
        else:
            if route.is_method_allowed(request_method):
                return route.handler
            else:
                raise HTTPException(HTTPStatus.METHOD_NOT_ALLOWED)
                
    def handle_request(self, request):
        response = Response() 
        try :
            route , kwargs = self.find_route(request.path)
            handler = self.get_handler(route, request.method)
            self._process_middleware_request(request, response)
            handler(request,response, **kwargs)
            self._process_middleware_response(request, response)
        except Exception as e:
            self._handle_exception(request, response, e)
        return response
    
    def _process_middleware_request(self, request,response):
        for middleware in self.middleware:
            middleware.process_request(request)

    def _process_middleware_response(self, request, response):
        for middleware in reversed(self.middleware):
            middleware.process_response(request, response)
        
    def _handle_exception(self, request, response, exception):
        exception_type = type(exception)
        handler = self.exception_handlers.get(exception_type)
        response.status = exception.status_code
        if handler:
            handler(request, response, exception)
        if not self.debug:
            raise exception
        debug_exception_handler(request, response, exception)
    
    def add_route(self, pattern, handler, allowed_methods):
        assert pattern not in self._routes, f"Route {pattern} already exists."
        # Store the path, handler, and allowed methods together
        self._routes[pattern] = Router(pattern, handler, allowed_methods)

