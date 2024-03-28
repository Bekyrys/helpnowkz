import os
from django.contrib.auth import authenticate, login

class PreAuthenticateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.username = os.environ.get('Glavadmin')
        self.password = os.environ.get('AdminParol0780')

    def __call__(self, request):
        if not request.user.is_authenticated:
            user = authenticate(request, username=self.username, password=self.password)
            if user is not None:
                login(request, user)
        response = self.get_response(request)
        return response
