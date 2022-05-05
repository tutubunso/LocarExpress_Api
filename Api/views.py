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
        #group: Group= Group.objects.get(id= data.get('group'))
        #user.groups.add(group)
        #user.save()
        personnel.save()
        serializer = PersonnelsSerializer(personnel,many=False).data
        return Response(serializer,201)

class CarburantViewSet(viewsets.ModelViewSet):
    serializer_class = CarburantSerializer
    permission_classes = IsAuthenticated,
    queryset = Carburant.objects.all().order_by('-id')

class EtatViewSet(viewsets.ModelViewSet):
    serializer_class = EtatSerializer
    queryset = Etat.objects.all().order_by('-id')
    permission_classes = IsAuthenticated,

class LocationViewSet(viewsets.ModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.all().order_by('-id')
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = IsAuthenticated,

    @transaction.atomic()
    def create(self,request):
        data = request.data
        user = request.user
        personnels=Personnels.objects.get(user=user)
        tarif:Tarif = Tarif.objects.get(id = int(data.get('tarif')))
        prix=tarif.prix_par_jour
        
        location1:Location = Location(
            personnels=personnels,
            locataire=data.get('locataire'),
            duree_location=data.get('duree_location'),
            prix_paye=data.get('prix_paye'),
            )

        location1.prix_a_paye=(float(location1.duree_location)*prix)
        location1.dettes=location1.prix_a_paye-float(location1.prix_paye)

        location1.user=request.user
        location1.save()

        return Response({"status":"location effectue avec success"},201)


class TarifViewSet(viewsets.ModelViewSet):
    serializer_class = TarifSerializer
    queryset = Tarif.objects.all().order_by('-id')
    permission_classes = IsAuthenticated,

class ChauffeurViewSet(viewsets.ModelViewSet):
    serializer_class = ChauffeurSerializer
    queryset = Chauffeur.objects.all().order_by('-id')
    permission_classes = IsAuthenticated,

class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    queryset = Document.objects.all().order_by('-id')
    permission_classes = IsAuthenticated,

class VoitureViewSet(viewsets.ModelViewSet):
    serializer_class = VoitureSerializer
    queryset = Voiture.objects.all().order_by('-id')
    permission_classes = IsAuthenticated,

class VoitureViewSet(viewsets.ModelViewSet):
    serializer_class = VoitureSerializer
    queryset = Voiture.objects.all().order_by('-id')
    permission_classes = IsAuthenticated,
