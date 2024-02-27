from django.shortcuts import HttpResponse, render
from django.template.response import TemplateResponse
from .models import Post
# function based middleware
def my_middleware(get_responce):
    print("One Time function Initialization")
    def my_func(request):
        print("I'm function Executing before  the request is handled.")
        response = get_responce(request)
        print("I'm function  executing after the request has been handled.")
        return response
    return my_func

# class based middleware
class MyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        print("One Time class Initialization")
    def __call__(self, request):
        print("I'm class Executing before  the request is handled.")
        response = self.get_response(request)
        print("I'm class  executing after the request has been handled.")
        return response

# process based middleware
class MyProcessMiddleware:
    def __init__(self, get_responce) -> None:
        self.get_responce = get_responce
        self.visits = 0
        self.no_of_posts = 0
    def __call__(self, request):
        """
        Processes a request by calling all of its process methods in order. If any process method returns a value that is not an instance of `HttpResponse`, it must be converted to one.
        Processes a request by calling all of its process methods in turn. If any process method returns a value that is not `None`, then it is returned immediately, and no further processing is
        Calls passed callable processing the given request.
        The result will be returned as if it was called directly.
        If an exception occurs in the process of calling the target,
        that exception will be propagated instead of the original one.
        """
        self.visits += 1
        self.no_of_posts = Post.objects.all().count()
        try:
            response = self.get_responce(request)
        except Exception as e:
            response = HttpResponse('An error occurred while processing your request as',e)
            response['Content-Type'] = 'text/plain'
        finally:
            return response
    
    def  process_view(self, request, view, *args, **kwargs):
        responce = HttpResponse("This is before view")
        responce = None
        return responce
    def process_exception(self, request, exception):
        class_name = exception.__class__.__name__
        return HttpResponse("Exception occured : {}, of exception class {}".format(str(exception),str(class_name)))
    
    def process_template_response(self,request, response):
        try:
            response.context_data['visits']=self.visits
            response.context_data['no_of_posts']=self.no_of_posts
        except:
            pass
        # print("process template is running",'*'*9) 
        # print(request)
        return response