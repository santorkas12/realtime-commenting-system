from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

class LoginService(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, **{'username': username, 'password': password})

        if user:
            login(request, user)
            response = Response(
                {'result': 'Success', 'message': 'Authenticated Successfully'},
                content_type='application/json'
            )
            response.set_cookie('sessionid', request.session.session_key)
            return response
        else:
            return Response({'result': 'Fail', 'message': 'Invalid credentials'}, content_type='application/json', status=400)
