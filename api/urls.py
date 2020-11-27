from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from .views import *

app_name = 'api_app'

urlpatterns = [
    path('', postlist, name = 'homeapi'),
    #path('', PostList.as_view(), name = 'homeapi'),
    path('<int:pk>/', PostDetail.as_view(), name = 'singleapi'),
    path('<int:pk>/do',Apithings.as_view(),name= 'do')
]