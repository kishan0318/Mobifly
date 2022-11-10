from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
# from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .authentication import ExpiringTokenAuthentication
from .serializers import *
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.decorators import authentication_classes,permission_classes
import pytz
import datetime
# Create your views here.

class SignupApi(generics.CreateAPIView):
    permission_classes=[AllowAny]
    queryset=User.objects.all()
    serializer_class=SignupSer


class Login(generics.GenericAPIView):
    queryset=User.objects.all()
    def post(self,request,*args,**kwargs):
        username=request.data.get('username')
        password=request.data.get('password')
        qs=authenticate(username=username,password=password)
        if not qs:
            return Response({'message':"User not found"},400)
        else:

            utc_now=datetime.datetime.utcnow()
            utc_now=utc_now.replace(tzinfo=pytz.utc)
            Token.objects.filter(user=qs,created__lt=utc_now-datetime.timedelta(minutes=1)).delete()

            token , _ =Token.objects.get_or_create(user=qs)
            token.save()
            data={'username':qs.username,'token':token.key}
            return Response({'data':data},200)

#this was created to check if token authentication is working or not
@permission_classes([IsAuthenticated])
@authentication_classes([ExpiringTokenAuthentication])
class SignupApiAdmin(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class=SignupSer                    
