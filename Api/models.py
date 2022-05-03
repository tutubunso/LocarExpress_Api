from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from datetime import datetime,timedelta
from django.core.validators import MinValueValidator
from django.db.models import Q

class Personnels(models.Model):
	id = models.AutoField(primary_key = True)
	user = models.OneToOneField(User,on_delete=models.PROTECT)
	adresse = models.CharField(max_length =100)
	telephone = models.FloatField()
	cni = models.FloatField()

	def __str__(self):
		return f" Nom:{self.user.first_name} CNI :{self.cni} Adresse :{self.adresse}"

class Carburant(models.Model):
	id = models.AutoField(primary_key=True)
	nom =  models.CharField(max_length=100)

	def __str__(self):
		return f"Nom:{self.nom}"

class Etat(models.Model):
	id = models.AutoField(primary_key=True)
	nom =  models.CharField(max_length=100)

	def __str__(self):
		return f"Nom:{self.nom}"

class Voiture(models.Model):
	id = models.AutoField(primary_key=True)
	promoteur = models.ForeignKey(Personnels, related_name='person_promo',on_delete=models.CASCADE,blank=True)
	consomation = models.ForeignKey(Carburant, related_name='conso_carbu',on_delete=models.CASCADE,blank=True)
	etat = models.ForeignKey(Etat, related_name='etat_voiture',on_delete=models.CASCADE,blank=True)
	marque =  models.CharField(max_length=100)
	place =  models.IntegerField()
	plaque =  models.CharField(max_length=200,null=True)
	vendu = models.BooleanField()
	location = models.BooleanField()
	date_arrive =  models.DateField()

	def __str__(self):
		return f"Marque:{self.marque} Place:{self.place} Plaque:{self.plaque}"

class Document(models.Model):
	id = models.AutoField(primary_key=True)
	voiture = models.ForeignKey(Voiture, related_name='docu_voiture',on_delete=models.CASCADE,blank=True,editable=False)
	carte_grise = models.CharField(max_length=150)
	carte_rose =  models.CharField(max_length=100)
	assurance =  models.CharField(max_length=150)
	controle_technique =  models.CharField(max_length=28)

	def __str__(self):
		return f"Carte Grise:{self.carte_grise} Carte Rose:{self.carte_rose}"