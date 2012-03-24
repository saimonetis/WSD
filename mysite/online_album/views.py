from django.template.loader import get_template
from django.template import Context
from django.http import Http404,HttpResponse,HttpResponseRedirect
from django.utils import simplejson
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from mysite.online_album.models import AlbumUserProfile, Album, Friends, Picture
from django.contrib.auth.models import User
from online_album.RegisterUser import RegisterUser
from django.db import IntegrityError

import Image

#this function authenticates user's login
#if username and password are correct, user is redirected to home page
#if not, user stays on the login page
@csrf_exempt
def main(request):
	snap = {}
	username=''
	if request.user.is_authenticated():
		username = request.user.username
		usertemp =request.user
		#login(request, usertemp)
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
			friendProfileId=friendIndividual.friendID.user.id#id in User!!!!!!!!!!!!!!!!!!!!!!!
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
		return render_to_response('homePage.html',{'curUser':curUser,'friends':friends,'acquaintances':acquaintances})
		#else:
		#	state = "Your account is not active, please contact the site admin."    	
	
	return render_to_response('full-width' + '.html', {"username":username, "snap":snap})

#this function adds new liked people to current user
def addNewLikePeople_func(request):
	if request.is_ajax() and request.method=='GET':
		ids=request.GET.get('ids')
		idcopy=[]
		for item in ids:
			idcopy.append('*'+item)
		data={'idcopy':idcopy}
	json=simplejson.dumps(data)
	return HttpResponse(json, mimetype='application/json')
	
#previous page for right arrow on "showAlbumPage.html"
#when user clicks on the right arrow, this function fetches images on previous page
def previousPage(request):
	picsOnRequiredPage=[]
	#fetching images uses ajax way
	if request.is_ajax() and request.method=='GET':
		albumIDValue=int(request.GET.get('albumID'))
		pageNumValue=request.GET.get('pageNum')
		#find all images belonging to alubm with id 'albumIDValue'
		picsOfAlbum=Picture.objects.filter(albumID=albumIDValue)
		#check if there are more pictures belonging to page with page number "pageNumValue"
		isMorePic='false'
		for pic in picsOfAlbum:
			if pic.pagesID==pageNumValue:
				isMorePic='true'
		#no more pictures
		if isMorePic=='false':
			data={'firstPage':'true'}
			json1=simplejson.dumps(data)
			return HttpResponse(json1, mimetype='application/json')
		
		#record layout id, name and description information about each picture
		for pic in picsOfAlbum:
			if pic.pagesID == pageNumValue:
				singlePic={}
				singlePic['layoutID']=pic.layoutID
				singlePic['img_holder']=pic.img_holder
				singlePic['layoutNameID']=pic.layoutNameID
				singlePic['layoutDescrID']=pic.layourDescrID
				singlePic['picUrl']=pic.picUrl
				singlePic['pictName']=pic.pictName
				singlePic['pictDescription']=pic.pictDescription
				picsOnRequiredPage.append(singlePic)
		data={'pics':picsOnRequiredPage,'firstPage':'false'}
	json=simplejson.dumps(data)
	return HttpResponse(json, mimetype='application/json')
	
#next page for right arrow on "showAlbumPage.html"
#when user clicks on the left arrow, this function fetches images on the next page
def nextPage(request):
	picsOnRequiredPage=[]
	if request.is_ajax() and request.method=='GET':
		albumIDValue=int(request.GET.get('albumID'))
		pageNumValue=request.GET.get('pageNum')
		picsOfAlbum=Picture.objects.filter(albumID=albumIDValue)
		#check if there are pictures on the page with page number 'pageNumValue'
		isMorePic='false'
		for pic in picsOfAlbum:
			if pic.pagesID==pageNumValue:
				isMorePic='true'
		#no more pictures
		if isMorePic=='false':
			data={'lastPage':'true'}
			json1=simplejson.dumps(data)
			return HttpResponse(json1, mimetype='application/json')
			
		#record layout id, name and description information about each picture
		for pic in picsOfAlbum:
			if pic.pagesID == pageNumValue:
				singlePic={}
				singlePic['layoutID']=pic.layoutID
				singlePic['img_holder']=pic.img_holder
				singlePic['layoutNameID']=pic.layoutNameID
				singlePic['layoutDescrID']=pic.layourDescrID
				singlePic['picUrl']=pic.picUrl
				singlePic['pictName']=pic.pictName
				singlePic['pictDescription']=pic.pictDescription
				picsOnRequiredPage.append(singlePic)
		data={'pics':picsOnRequiredPage,'lastPage':'false'}
	json=simplejson.dumps(data)
	return HttpResponse(json, mimetype='application/json')

#redirect user to the profile page
def profile_func(request,user_id):
	try:
		user_id=int(user_id)
	except ValueError:
		raise Http404()
	t=get_template('profile.html')
	html=t.render(Context({'user_id':user_id}))
	return HttpResponse(html)

#log out user
def logout_func(request):
	t=get_template('logout.html')
	html=t.render(Context({'logout_info':'You have successfully logged out!'}))
	return HttpResponse(html)
#add a new page to the album with id 'albumID'
def addNewPage_func(request,curUserID,albumID):
	album=Album.objects.get(userID=curUserID)
	albumCoverPic=album.albumCoverPicture
	albumName=album.albumName
	albumDesc=album.albumDescription
	
	try:
		albumID=int(albumID)
	except ValueError:
		raise Http404()
	t=get_template('addNewPage.html')
	html=t.render(Context({'curUserID':curUserID,'default_pic':albumCoverPic,'albumName':albumName,'albumDesc':albumDesc}))
	return HttpResponse(html)
#upload cover image of an album
@csrf_exempt
def uploadAlbumCoverImage_func(request,userId):
	if request.method=='POST':
		#get uploaded image, current logged-in user's id, current user name
		image=request.FILES['inputAlbumCoverImage'];
		curUserID=request['curUserID']
		curUserName=request['curUserName']
		
		t=get_template('addNewPage.html')
		html=t.render(Context({}))
		return HttpResponse(html)
#create a new album
#this function gives basic information when the user first enter into the create new album page
def createNewAlbum_func(request, curUserID):
	try:
		userID=int(curUserID)
	except ValueError:
		raise Http404()
	userName=User.objects.get(id=userID).username
	curUser={}
	curUser['id']=userID
	curUser['name']=userName
	curAlbumID=Album.objects.get(userID=curUserID).id
	albumName="enter your album name"
	albumDesc="enter your description for the album"
	default_pic="defaultGalleryPic.jpg"
	
	t=get_template('addNewPage.html')
	html=t.render(Context({'curUser':curUser,
						   'albumName':albumName,
						   'albumID':curAlbumID,
						   'albumDesc':albumDesc,
						   'default_pic':default_pic}))
	return HttpResponse(html)

#this function fetches information of users that current logged-in user likes and might like
#and use these information to populate the homePage.html
def homePage_func(request, loginUserID):
	t=get_template('homePage.html')
	#get logged-in user's profile picture
	usertemp=User.objects.get(id=loginUserID)
	profile=usertemp.get_profile().profile_pic
	profileID=usertemp.get_profile().id #id in albumuserprofile table
	username=usertemp.username	
	#get logged-in user's albums
	albumList=Album.objects.filter(userID=loginUserID)
	albums={}
	for item in albumList:
		albums[item.id]=item.albumName
	curUser={'id':loginUserID,'name':username,'profile':profile,'albums':albums}
					
	#get logged-in user's friends
	friendList=Friends.objects.filter(currentID=profileID)
	friends=[]
	for friendIndividual in friendList:#contain records in friends
		friendDict={}
		#get friend id of current user
		friendProfileId=friendIndividual.friendID.user.id#id in User
		friendid=friendProfileId#user_id in albumuserprofile
		friendIdInUser=AlbumUserProfile.objects.get(id=friendid).user.id#user_id in albumuserprofile
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
	friendid_list.append(usertemp.id)
	#all the users that are not liked by current logged in user are viewed as people that current user might like
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
				
	html=t.render(Context({'curUser':curUser,'friends':friends,'acquaintances':acquaintances}))
	return HttpResponse(html)

#this function returns images of the first album page of an album with id 'albumIDValue'
def showAlbumPage_func(request,albumIDValue,loginUserID):
	try:
		albumIDValue=int(albumIDValue)
	except ValueError:
		raise Http404()
	
	t=get_template('showAlbumPage.html')
	albumInfo=Album.objects.get(id=albumIDValue)
	albumName=albumInfo.albumName
	albumDesc=albumInfo.albumDescription
	default_pic=albumInfo.albumCoverPicture
	
	leftArrow="leftArrow.jpg"
	rightArrow='rightArrow.jpg'
	#get all pictures with albumID='albumIDValue'
	albumPageInfo=Picture.objects.filter(albumID=albumIDValue)
	firstPageOfAlbum=[]
	#find all images on the first album page(page number is 0)
	for pic in albumPageInfo:
		if pic.pagesID== "0":
			firstPageOfAlbum.append(pic)
	layout_id=firstPageOfAlbum[0].layoutID
	#find the layout the first album page uses
	if layout_id==2:
		layout_temp="layout2.html"
	else:
		layout_temp="layout3.html"
	#fetch the layout information, name and description of each image on the first album page
	albumPage={}
	for pic in firstPageOfAlbum:
		if layout_id==2:
			if pic.layoutNameID=="pic_name1_layout2":
				albumPage['img_layout2_1']=pic.picUrl
				albumPage['pic_name1_layout2']=pic.pictName
				albumPage['pic_description1_layout2']=pic.pictDescription
			elif pic.layoutNameID=="pic_name2_layout2":
				albumPage['img_layout2_2']=pic.picUrl
				albumPage['pic_name2_layout2']=pic.pictName
				albumPage['pic_description2_layout2']=pic.pictDescription
		elif layout_id==3:
			if pic.layoutNameID=="pic_name1_layout3":
				albumPage['img_layout3_1']=pic.picUrl
				albumPage['pic_name1_layout3']=pic.pictName
				albumPage['pic_description1_layout3']=pic.pictDescription
			elif pic.layoutNameID=="pic_name2_layout3":
				albumPage['img_layout3_2']=pic.picUrl
				albumPage['pic_name2_layout3']=pic.pictName
				albumPage['pic_description2_layout3']=pic.pictDescription
			elif pic.layoutNameID=="pic_name3_layout3":
				albumPage['img_layout3_3']=pic.picUrl
				albumPage['pic_name3_layout3']=pic.pictName
				albumPage['pic_description3_layout3']=pic.pictDescription
	curUserName=User.objects.get(id=loginUserID).username
	html=t.render(
		Context({'curUser':{'id':loginUserID,'name':curUserName},
				 'albumID':albumIDValue,
				 'pagesID':"0",
				 'layout_temp':layout_temp,
				 'default_pic':default_pic,
			     'albumName':albumName,
			     'albumDesc':albumDesc,
				 'leftArrow':leftArrow,
				 'rightArrow':rightArrow,
				 'albumPage':albumPage}))
	return HttpResponse(html)


def about(request):

	if request.user.is_authenticated():
		username = request.user.username
	else:
		username = None
	
	return render_to_response('about2.html', {"user":username})
	
	
	
def register(request):

	username = request.user.username


	if username: # si hay alguien logueado se lo digo
		
		explan = "You are already registered in this application."
		return render_to_response('error.html', {"descript":"WARNING", "explan":explan, "user":username})
		
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
				return render_to_response('register2.html', {"form":form, "mismatch":mismatch, "user":username})
			
			try:
				user = User.objects.create_user(nick, mail, passwd1)
				profile=AlbumUserProfile(user=user,profile_pic="male_final.jpeg")
				profile.save()

				return render_to_response('response_post.html', {"explan": '<center><h2><font color="green">ACCOUNT CREATED</font></h2></center>', "user":username})

			except IntegrityError:
				explan = "Username ( " + nick + ' ) is already in use<br>Try another one<br> <a href="/register" title = "Volver">Back</a>'
				return render_to_response('error.html', {"descript":"WARNING", "explan":explan, "user":username})

	else: # Get
			form = RegisterUser()
	return render_to_response('register2.html', {
		'form': form, "user":request.user.username
	})


