from promises.models import Promise
from promises.serializers import PromiseSerializer
from promises.serializers import PromiseUpdateSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from promises.serializers import UserSerializer
from promises.serializers import UserAllSerializer
from rest_framework import permissions
from promises.permissions import IsOwnerOrReadOnly
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
            'id': user.id
        })

class PromiseList(generics.ListCreateAPIView):
    queryset = Promise.objects.all()
    serializer_class = PromiseSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def perform_create(self, serializer):
    	serializer.save(user1=self.request.user)

class PromiseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Promise.objects.all()
    serializer_class = PromiseSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly,)
    def get_serializer_class(self):
        if self.request.method in ['PUT','PATCH']:
            return PromiseUpdateSerializer
        return self.serializer_class

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserAllList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserAllSerializer

class UserAllDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserAllSerializer
