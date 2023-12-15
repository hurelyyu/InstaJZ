from django.contrib import admin 
#connect with django admin, tell django admin which need to be show on admin page
from Insta.models import Post, InstaUser, Like, UserConnection
#from Insta.models import PostTwo
# Register your models here.
admin.site.register(Post)
admin.site.register(InstaUser)
admin.site.register(Like)
admin.site.register(UserConnection)
