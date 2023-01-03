from django.shortcuts import render

from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework.response import Response

class RegisterView(CreateAPIView) :
    queryset = User.objects.all()
    serializer_class=RegisterSerializer

    def post(self,request, *args, **kwargs) :
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True) #Hata varsa ilerleme, ahta yoksa devam et anlamina geliyor.
        serializer.save()

        return Response(
            {
                "message" : "User Created!",
                "username" : request.data.get("username"),
                "email" : request.data.get("email"),
                
            }
        )