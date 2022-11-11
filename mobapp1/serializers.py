from rest_framework.serializers import *
from django.contrib.auth.models import User
from rest_framework.fields import CharField

class Signup(ModelSerializer):
    class Meta:
        model=User
        fields=["username","password","first_name","last_name"]

class SignupSer(Serializer):
    username=CharField(required=True)
    password=CharField(required=True)
    first_name=CharField(required=True)
    last_name=CharField(required=True)
    def validate(self,data):
        qs=User.objects.filter(username=data.get('username')).first()
        if qs:
            raise ValidationError("Username already exists")
        
        return data

    def create(self,validated_data):
        username=validated_data.get('username')
        password=validated_data.get('password')
        first_name=validated_data.get('first_name')
        last_name=validated_data.get('last_name')
        qs=User.objects.create_user(username=username,last_name=last_name,first_name=first_name)
        qs.set_password(password)
        qs.save()
        return validated_data
