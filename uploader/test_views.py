from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, TestCase

from .views import VideoViewset

def add_middleware_to_request(request, middleware_class):
    middleware = middleware_class()
    middleware.process_request(request)
    return request

def add_middleware_to_response(request, middleware_class):
    middleware = middleware_class()
    middleware.process_response(request)
    return request

class VideoViewsetTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    
    def test_list(self):
        request = self.factory.get('/videos/')
        request.user = AnonymousUser()
        request = add_middleware_to_request(request, SessionMiddleware)
        request.session.save()
        
        response = VideoViewset.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)