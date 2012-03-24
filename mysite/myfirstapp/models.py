from django.db import models
from django.contrib.auth.models import User
# Create your models here.


#USER TABLE
class User1(models.Model):
	userID = models.CharField(max_length=256)
	userName = models.CharField(max_length=256)
	email =  models.CharField(max_length=256)
	password =  models.CharField(max_length=64)
	#here should it be profilePicture

#ALBUM TABLE
class Album (models.Model):
	albumID = models.CharField(max_length=256, primary_key='True') # te lo genera django solo
	albumName = models.CharField(max_length=256)
	albumDescription = models.TextField()
	#each album is asociated to one user	
	userID = models.ForeignKey(User1)
	# falta album cover (URL)
	hit = models.IntegerField()

#PICTURE TABLE
class Picture (models.Model):

	pictID = models.CharField(max_length=256, primary_key='True')
	albumID = models.ForeignKey(Album)
	layoutID = models.IntegerField()
	pictName = models.CharField(max_length=256)
	pictDescription = models.TextField()
	pagesID = models.CharField(max_length=256)
	layoutNameID = models.CharField(max_length=64)
	layourDescrID = models.CharField(max_length=256)
	
#FRIEND TABLE

class Friends (models.Model):
	currentID = models.CharField(max_length=15)
	friendID = models.CharField(max_length=15)

