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