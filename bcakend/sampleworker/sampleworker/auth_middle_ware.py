import requests
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


class CustomError(Exception):
    def __init__(self, data, status_code):
        self.data = data
        self.status_code = status_code
        super().__init__(data)


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed before the view is called

        get_auth = request.headers.get("Auth", None)

        response = self.get_response(request)
        if not get_auth:
            response = Response(
                data='You are not login',
                status=status.HTTP_401_UNAUTHORIZED
            )
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = "application/json"
            response.renderer_context = {}
            response.render()
            return response
        check_login_status = requests.post("http://localhost:8000/accounts/verify/",
                                           data={"token": get_auth})
        if check_login_status.status_code == 400:
            response = Response(
                data='You are not login',
                status=status.HTTP_401_UNAUTHORIZED
            )
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = "application/json"
            response.renderer_context = {}
            response.render()
            return response


        elif check_login_status.status_code == 200:
            return response
