from rest_framework import serializers, validators
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer) :


    email = serializers.EmailField(
        required=True,
        validator = [validators.UniqueValidator(queryset=User.objects.all())] #Unique validatoru hazir kullanicilar icinde kiyaslattiriyorum. 
        )


    password = serializers.CharField(
        required=True, 
        write_only=True, #write_only=True yapmamin sebebi yazmak zorunlu olsun ama gözükmesin.
        validator = [validate_password]  
        ) 


    password2 = serializers.CharField(
        required=True,
        write_only=True,
        validator = [validate_password]   
         )


    class Meta :
        model = User
        exclude = []

    #override yapiyorum
    def validate (self,attrs) :
        if attrs['password'] == attrs['password2'] :
            raise serializers.ValidationError({"message":"Passwords are not same!"})
        return attrs
#Bu fonksiyona gelmeden önce yukardaki bilgiler dogrulanmis olacak. 
    def create(self, validated_data) :
        password = validated_data.get('password')
        validated_data.pop('password2') ##Onaylandiktan sonra artik password2 yi silebilirim. DB'ye kaydedilmesine gerek yok
        user = User.objects.create(**validated_data)