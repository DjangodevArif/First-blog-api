from django.contrib import admin
from .models import Profile, Post, Coment, Co_coment

# Register your models here.


admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Coment)
admin.site.register(Co_coment)
# admin.site.register(Like)