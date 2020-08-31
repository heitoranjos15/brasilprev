# from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets
from rest_framework import authentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .models import Product
from .serializers import UserSerializer, ProductSerializer, OrderSerializer


User = get_user_model()


class AuthMixin(object):
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
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
        IsAdminUser,
    )


class OrderCreate(AuthMixin, generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = OrderSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return HttpResponse(status=201)
