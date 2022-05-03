from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from django.db import transaction
from .serializers import *
from .models import *
from datetime import datetime,timedelta
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Avg

class TokenPairView(TokenObtainPairView):
    serializer_class = TokenPairSerializer

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('-id')

class GroupViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = IsAuthenticated,
    queryset = Group.objects.all().order_by('-id')
    serializer_class = GroupSerializer

class PersonnelsViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = IsAuthenticated,
    serializer_class = PersonnelsSerializer
    queryset = Personnels.objects.all().order_by('-id')


    @transaction.atomic()
    def create(self,request):
        data = request.data
        station:Station = Station.objects.get(id = int(data.get('station')))

        user = User(
            username = data.get('user.username'),
            first_name = data.get('user.first_name'),
            last_name = data.get('user.last_name')
        )
        user.set_password(data.get('user.password'))
        personnel = Personnels(
            user = user,
            adresse=data.get('adresse'),
            telephone=data.get('telephone'),
            cni=data.get('cni'),

            )
        user.save()
        #group = data.pop('group')
        group: Group= Group.objects.get(id= data.get('group'))
        user.groups.add(group)
        user.save()
        personnel.save()
        serializer = PersonnelsSerializer(personnel,many=False).data
        return Response(serializer,201)