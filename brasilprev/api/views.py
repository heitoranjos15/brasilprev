# from django.shortcuts import render

# Create your views here.
from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .models import Product
from .serializers import UserSerializer, ProductSerializer


User = get_user_model()


class AuthMixin(object):
    authentication_classes = (
        BasicAuthentication,
        TokenAuthentication,
    )


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )


class ProductViewSet(AuthMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdminUser
    )
