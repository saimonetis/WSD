from django.db import models
from django.contrib.auth.models import User

#USER TABLE containing all profile picture URLs of all users 
class AlbumUserProfile(models.Model):
	user=models.ForeignKey(User,unique='True')
	#profile picture of user
	profile_pic=models.CharField(max_length=256)	
	def __unicode__(self):
		return self.user.username

#ALBUM TABLE containing all the albums information of all users
class Album (models.Model):
	#album name
	albumName = models.CharField(max_length=256)
	#album description
	albumDescription = models.TextField()
	#each album is asociated to one user	
	userID = models.ForeignKey(User)
	#this column contains album cover picture URL
	albumCoverPicture=models.CharField(max_length=256)
	#status indicating album is public or private
	status=models.CharField(max_length=50)
	#numbers of times that album is visited
	hit = models.IntegerField()
	def __unicode__(self):
		return self.albumName

#PICTURE TABLE containing all the pictures of all albums
class Picture (models.Model):
	#album id
	albumID = models.ForeignKey(Album)
	#layout template id to indicate which layout this picture uses
	layoutID = models.IntegerField()
	#picture name
	pictName = models.CharField(max_length=256)
	#picture description
	pictDescription = models.TextField()
	#page number to indicate which album page this picture to be shown
	pagesID = models.CharField(max_length=256)
	#id storing which name box this picture name is put into
	layoutNameID = models.CharField(max_length=64)
	#id storing which description box this picture description is put into
	layourDescrID = models.CharField(max_length=256)
	#picture URL to access real picture in the image folder
	picUrl=models.CharField(max_length=256)
	#id storing which img element this picture is put into
	img_holder=models.CharField(max_length=64)
	def __unicode__(self):
		return self.pictName
	
#FRIEND TABLE containing "like" relationship between users
class Friends (models.Model):
	#user id indicating current logged-in user
	currentID = models.ForeignKey(AlbumUserProfile, related_name='friends_currentID')
	#user id indicating all people that are liked by current logged-in user
	friendID = models.ForeignKey(AlbumUserProfile,related_name='friends_friendID')
	def __unicode__(self):
		return self.currentID.user.username
