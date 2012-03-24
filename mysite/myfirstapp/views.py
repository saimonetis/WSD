# Create your views here.
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import *
from myfirstapp.models import User1, Album, Picture, Friends
from myfirstapp.RegisterUser import RegisterUser
from datetime import *
from django.db import IntegrityError
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.html import escape

#Main

#VIEWS
def main(request):

    snap = {}

	#Se que el problema esta aqui. 
    if request.user.is_authenticated():
    	usertemp = request.user.username
	if request.user:
		#get logged-in user's id
				#id in auth_user
				userid=usertemp.id
				#get logged-in user's profile picture
				profile=usertemp.get_profile().profile_pic
				profileID=usertemp.get_profile().id #id in albumuserprofile table
				
				#get logged-in user's albums
				albumList=Album.objects.filter(userID=userid)
				albums={}
				for item in albumList:
					albums[item.id]=item.albumName
				curUser={'id':userid,'name':username,'profile':profile,'albums':albums}
					
				#get logged-in user's friends
				friendList=Friends.objects.filter(currentID=profileID)
				friends=[]
				for friendIndividual in friendList:#contain records in friends
					friendDict={}
					#get friend id of current user
					friendProfileId=friendIndividual.friendID.user.id#id in User
					friendid=User.objects.get(id=friendProfileId).id#user_id in albumuserprofile
					friendIdInUser=friendid
					friendDict['id']=friendIdInUser
					
					friend=User.objects.get(id=friendIdInUser)
					#get friend name
					friendName=friend.username
					friendDict['name']=friendName
					#get friend's profile picture
					profilePic=friend.get_profile().profile_pic
					friendDict['profile']=profilePic
					friendAlbumList=Album.objects.filter(userID=friendid)
					friendAlbum={}
					for item in friendAlbumList:
						friendAlbum[item.id]=item.albumCoverPicture
					friendDict['albums']=friendAlbum
					friends.append(friendDict)
				#find acquaintances
				acquaintances={}
				friendid_list=[]#contain all frined ids of current user
				for item in friends:
					friendid_list.append(item['id'])
				friendid_list.append(userid)
				
				album_list=Album.objects.all()
				acquaitanceAlbum_list=[]
				for item in album_list:
					if item.userID.id not in friendid_list:
						acquaitanceAlbum_list.append(item)
				for item in acquaitanceAlbum_list:
					acquaitanceID=item.userID.id
					acquaintanceName=item.userID.username
					acquaintanceProfilePic=item.userID.get_profile().profile_pic
					acquaintances[acquaitanceID]=[acquaintanceName,acquaintanceProfilePic]
				#the user is valid and is redirected to the home page
				return render_to_response('/home/dongshichao/djcode/mysite/online_album/templates/homePage.html',{'curUser':curUser,'friends':friends,'acquaintances':acquaintances})
			#return HttpResponseRedirect("/"+ user + "/")
    else:
    	user = None
	
	return render_to_response('full-width' + '.html', {"user":user, "snap":snap})

def space(request, name):
	return render_to_response('space.html')

def main_user(request, name):
	return render_to_response('space.html')

# LOG IN OK
def logOK(request, name):
	return HttpResponseRedirect("/"+ name + "/")


##############----------------------------------------------------
def register(request):

	user = request.user.username


	if user: # si hay alguien logueado se lo digo
		
		explan = "You are already registered in this application."
		return render_to_response('error.html', {"descript":"WARNING", "explan":explan, "user":user})
		
	if request.method == 'POST': # If the form has been submitted...
		form = RegisterUser(request.POST) # A form bound to the POST data

		if form.is_valid(): # All validation rules pass
			nick = form.cleaned_data['name']
			mail = form.cleaned_data['mail']
			passwd1 = form.cleaned_data['passwd1']
			passwd2 = form.cleaned_data['passwd2']

			if passwd1 != passwd2:
				mismatch = True
				form = RegisterUser()
				return render_to_response('register2.html', {"form":form, "mismatch":mismatch, "user":user})

			try:
				user = User.objects.create_user(nick, mail, passwd1)
				return render_to_response('response_post.html', {"explan": '<center><h2><font color="green">ACCOUNT CREATED</font></h2></center>', "user":user})

			except IntegrityError:
				explan = "Username ( " + nick + ' ) is already in use<br>Try another one<br> <a href="/register" title = "Volver">Back</a>'
				return render_to_response('error.html', {"descript":"WARNING", "explan":explan, "user":user})

	else: # Get
			form = RegisterUser()
	return render_to_response('register2.html', {
		'form': form, "user":request.user.username
	})

####################################################
"""
#Register
def register(request):
	user = request.user.username
	# Is someone already using this aplication?
	if user:
		return render_to_response('error.html', {"description": "There is another user already using you account"})

	#If the form has been submitted
	if request.method == 'POST':
		form = RegisterUser(request.POST)
		if form.is_valid():
			name = form.cleaned_data['name']
			passwd1 = form.cleaned_data['passwd1']
			passwd2 = form.cleaned_data['passwd2']
			mail = form.cleaned_data['mail']
			if passwd1 != passwd2:
				#esto hay que cambiarlo
				mismatch = True
				form = RegisterUser()
				return render_to_response('register2.html', {"form":form, "mismatch":mismatch, "user":user})
			
			try:
				user = User.objects.create_user(name, mail, passwd1)
				return render_to_response('response_post.html', {"explan":'<center><h2><font color="green">ACCOUNT CREATED</font></h2>< center>',"user":user})

			except IntegrityError:
				return render_to_response('error.html', {"description":"the username you chose is already in use"})

	else:
		form = RegisterUser()
	return render_to_response('register2.html', {'form':form, "user":request.user.username})
"""
def about(request):

	if request.user.is_authenticated():
		user = request.user.username
	else:
		user = None
	
	return render_to_response('about2.html', {"user":user})

def hello(request):
	return HttpResponse("Hola, que tal?") # esto es una prueba

## -- Open ID



def index(request):
    s = ['<p>']
    if request.user.is_authenticated():
        s.append('You are signed in as <strong>%s</strong> (%s)' % (
                escape(request.user.username),
                escape(request.user.get_full_name())))
        s.append(' | <a href="/logout">Sign out</a>')
    else:
        s.append('<a href="/openid/login">Sign in with OpenID</a>')

    s.append('</p>')

    s.append('<p><a href="/private">This requires authentication</a></p>')
    return HttpResponse('\n'.join(s))


def next_works(request):
    return HttpResponse('?next= bit works. <a href="/">Home</a>')


@login_required
def require_authentication(request):
    return HttpResponse('This page requires authentication')

# -- Close OpenID

