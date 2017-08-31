from django.db import models

# Create your models here.
class Podatak(models.Model):
	ime			= models.CharField(max_length = 120)
	lokacija	= models.CharField(max_length = 120, null=True, blank=True)