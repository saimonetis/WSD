from django.contrib import admin
from mysite.online_album.models import AlbumUserProfile , Album, Picture, Friends

#class AlbumUserProfileAdmin(admin.ModelAdmin):
#	fields=['id','username']
#admin.site.register(AlbumUserProfile,AlbumUserProfileAdmin)
admin.site.register(AlbumUserProfile)

admin.site.register(Album)

admin.site.register(Picture)

admin.site.register(Friends)
