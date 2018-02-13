from snippets.models import User
from snippets.serializers import UserSerializer
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import login, authenticate
from rest_framework.settings import api_settings
from rest_framework_jwt.settings import api_settings
from django.views import View
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse


class UserList(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)


class UserDetails(APIView):
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)

    def patch(self, request, pk):
        return self.put(request, pk)

    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        if request.user.id != user.id:
            return HttpResponse(status=status.HTTP_403_FORBIDDEN)

        data = JSONParser().parse(request)
        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        if request.user.id != user.id:
            return HttpResponse(status=status.HTTP_403_FORBIDDEN)

        user.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class UserRegister(View):
    serializer_class = UserSerializer

    def post(self, request, format=None):
        data = JSONParser().parse(request)

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(View):
    def post(self, request):
        data = JSONParser().parse(request)
        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return JsonResponse({'status': 'Successful',
                                 'message': 'You have successfully been logged into your account.',
                                 'token': token
                                 }, status=status.HTTP_200_OK)

        return JsonResponse({
            'status': 'Unauthorized',
            'message': 'Username/password combination invalid.'
        }, status=status.HTTP_401_UNAUTHORIZED)
