from django.conf.urls.defaults import patterns, include, url
from mysite.online_album.views import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	('^$',main),
	(r'^login$', 'django.contrib.auth.views.login'),
	(r'^logout$', 'django.contrib.auth.views.logout'),
    (r'^about$',about),
    (r'^register$',register),
	url(r'^openid-login/$', 'django_openid_auth.views.login_begin', name='openid-login'),
	url(r'^login-complete/$', 'django_openid_auth.views.login_complete', name='openid-complete'),
	url(r'^openid-logout/$', 'django.contrib.auth.views.logout', {'next_page': '/',}, name='openid-logout'),
    ('^showAlbumPage/(\d+)/(\d+)/$',showAlbumPage_func),
    ('^home/(\d+)$',homePage_func),
    #('^logout/$',logout_func),
    ('^profile/(\d+)/$',profile_func),
    ('^admin/',include(admin.site.urls)),
    ('^nextAlbumPage/$',nextPage),
    ('^previousAlbumPage/$',previousPage),
    ('^createNewAblum/(\d+)/$',createNewAlbum_func),
    ('^upload/$',uploadAlbumCoverImage_func),
    ('^addNewLikePeople/$',addNewLikePeople_func),
)
