from django.urls import path
from .import views
# from Blog.views import NewPost

# this for auth login/logout functionlity

from  django.contrib.auth import views as auth_views

from .forms import LoginForm, PasswordReset


from .views import (Postlist, PostDetail,
    NewPost, PostUpdate, PostDelete, AuthorPost
    )
urlpatterns= [
    path('',Postlist.as_view(),name = 'home'),
    path('search/',views.search, name= 'search'),
    path('post/<str:author>/', AuthorPost.as_view(), name = 'authorpost'),
    path('like/',views.vote,name = 'like'),
    path('register/',views.register,name = 'register'),
    path('<int:pk>/', PostDetail.as_view() , name = 'post' ),
    path('sub-coment/', views.subcoment, name = 'sub-coment'),
    path('add_friend/', views.addfriends, name='addfriend'),
    path('remove_friend/',views.removefriend, name='removefriend'),
    path('request/',views.requestfriend, name='request'),
    path('activate/<uidb64>/<token>/',views.activate, name= 'activate'),
    path('<int:pk>/update', PostUpdate.as_view(), name = 'update'),
    path('<int:pk>/delete',PostDelete.as_view(),name = 'delete'),
    path('<int:pk>/comdel',views.comentdelete,name = 'com_del'),
    path('profile/',views.profile,name = 'profile'),
    path('newpost/', NewPost.as_view(), name='newpost'),
    path('login/',auth_views.LoginView.as_view(template_name = 'Blog/login.html',authentication_form=LoginForm),name = 'login'),
    path('logout/',auth_views.LogoutView.as_view(template_name = 'Blog/logout.html'),name = 'logout'),
            # when a user want to change Password intentionally the link works

    path('password_change/',auth_views.PasswordChangeView.as_view(template_name='Blog/password_change_form.html'),name='password_change'),
    path('password_change_done/',auth_views.PasswordChangeDoneView.as_view(template_name='Blog/password_change_done.html'),name= 'password_change_done'),
    
            # it is use for email verifaying  >>>>>>
    path('password-reset/',auth_views.PasswordResetView.as_view(
        template_name='Blog/password_reset.html',form_class=PasswordReset
    ),name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='Blog/password_reset_done.html'
    ),name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(
        template_name= 'Blog/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='Blog/password_reset_complete.html' ), name = 'password_reset_complete'), 
    
    
    
    
    
    
    
    
    
    
    
    
    #   for function based view
    # path('',views.get_name,name = 'home'),
    # path('<int:pk>/sub-coment/<int:id>/', views.subcoment, name = 'sub-coment'),
    # path('<int:pk>/',views.post,name = 'post'),
    # path('<int:pk>/update',views.postupdate,name = 'update'),
    # path('<int:pk>/delete',views.postdelete,name = 'delete'),
    # path('newpost/',views.newpost,name = 'newpost'),
    
    # path('password-reset/', auth_views.PasswordResetView.as_view(template_name='Blog/passreset.html'), name='password_reset'),
    # path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='Blog/passresetdone.html'), name='password_reset_done'),
    # path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='Blog/password_reset_confirm.html'), name='password_reset_confirm'),
    # path('password-reset-complete', auth_views.PasswordResetCompleteView.as_view(template_name='Blog/passwordresetcomplete.html' ), name = 'password_reset_complete'),
]
