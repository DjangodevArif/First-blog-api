from django.shortcuts import render,redirect, get_object_or_404
from .forms import (Userregister,UserUpdateForm,ProfileUpdateForm,
    ComentForm, NewPostForm, PostUpdateForm, Co_comentForm)
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils import timezone
import datetime

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse

from .models import Post, Coment, Profile
# Create your views here.
from django.contrib.auth.mixins import (LoginRequiredMixin,
 UserPassesTestMixin, PermissionRequiredMixin)
from django.views.generic import (ListView,
    DetailView, CreateView, UpdateView,
    DeleteView                                  )
# this import is necessery for verifying email before account acitivation
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import token_generator
from django.core.mail import EmailMessage
from django.conf import settings

class Postlist(ListView):
    model = Post
    template_name = 'Blog/home.html'
    ordering = ['-post_date']
    paginate_by = 4
    
    def get_context_data(self,**kwargs):
        friend = friend_count()
        context = super().get_context_data(**kwargs)
        context['friend_list'] = friend
        return context
    '''
    def get_name(request):
        post_list = Post.objects.all()
        paginator = Paginator(post_list, 3)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)


        return render(request,'Blog/home.html',{'page_obj': page_obj})'''


class PostDetail(DetailView):
    model = Post
    template_name = 'Blog/post.html'
    context_object_name = 'post'

    def comentpaginator(self,**kwargs):
        coment_list = self.object.coment_set.all()
        paginator = Paginator(coment_list, 3)
        page_number = self.request.GET.get('page',1)
        coment = paginator.page(page_number)
        return coment
        
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['c_form'] = ComentForm()
        context['co_form'] = Co_comentForm()
        context['coment_list'] = self.comentpaginator(**kwargs)
        return context

    def post(self, request,**kwargs):
         
        co_form = Co_comentForm(request.POST)
        c_form = ComentForm(request.POST)
 
        if 'up_coment' in request.POST:
            sel_coment = Coment.objects.get(id = request.POST['comentid'])
            sel_coment.coment_detail = str(request.POST['coment'])
            sel_coment.save()
            return redirect(request.META.get('HTTP_REFERER'))
            
        if 'sub_coment' in request.POST:
            main_coment = Coment.objects.get(id = self.request.POST['comentid'])  
            if co_form.is_valid(): 
                co_form.instance.coment_author = self.request.user
                co_form.instance.main_coment = main_coment
                co_form.save()      
                return redirect(reverse('post',args=(self.get_object().id,)))

        if 'coment' in request.POST:
            print(request.POST)
            if c_form.is_valid():
                c_form.instance.coment_author = self.request.user
                c_form.instance.postid = self.get_object()
                c_form.save()
                return redirect(reverse('post',args=(self.get_object().id,)))     
 
    '''def post(request, pk):

        post = Post.objects.get(pk = pk)
        coment_list = Coment.objects.filter(postid = pk)
        try:
            com = post.coment_set.get(coment_author = request.user)
        except:
            None
        form = None
        if request.user.is_authenticated:
            if request.method == 'POST':
                try:
                    com = post.coment_set.get(coment_author = request.user)      # এই পোস্টে উজার এর কমেন্ট থাকলে
                    # >>>>request.user == com.coment_author
                    form = ComentForm(request.POST,instance=com)         #<<<<,instance=com 
                except:
                    form = ComentForm(request.POST)
                form.instance.coment_author = request.user
                form.instance.postid = Post.objects.get(id= pk)
                if form.is_valid():
                    form.save()
                    return redirect(reverse('post',args=(pk,)))
            else:
                try:
                    com = post.coment_set.get(coment_author = request.user)   

                    form = ComentForm(instance=com)         #<< instance
                except:
                    form = ComentForm()
                form.instance.coment_author = request.user
                form.instance.postid = Post.objects.get(id=pk)

        return render(request,'Blog/post.html',{'form':form,'post':post,'coment_list':coment_list})
    '''

class AuthorPost(ListView):
    
    template_name = 'Blog/user_post.html'
    paginate_by = 4

    def get_queryset(self):
        author = get_object_or_404(User,username=self.kwargs.get('author'))
        return Post.objects.filter(post_author=author).order_by('-post_date')
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = get_object_or_404(User,username=self.kwargs.get('author'))
        return context


class NewPost(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['post_img', 'post_title', 'post_detail'] 


    def form_valid(self, form):
        form.instance.post_author = self.request.user
        return super().form_valid(form)

        # You can also use get_absulote_url() in Post model
    def get_success_url(self):
        return reverse('post', kwargs={'pk': self.object.pk})

    '''@login_required
    def newpost(request):
        if request.method == 'POST': 
            form = NewPostForm(request.POST,request.FILES)    
            form.instance.post_author = request.user
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/blog/')
        else:
            form = NewPostForm(request.POST,request.FILES)    
            form.instance.post_author = request.user


        return render(request,'Blog/post_form.html',{'form':form})
    '''


class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ('post_img', 'post_title', 'post_detail')
    # it`s take default template from above NewPost class(Creatview)
    template_name = 'Blog/postupdate.html'  # it depend as your wish
    
    def get_success_url(self):
        return reverse('post', kwargs={'pk': self.object.pk})
    

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.post_author:
            return True
        return False

    '''def postupdate(request,pk):
        a = Post.objects.get(id =pk)        
        if request.user == a.post_author:
            up_post = Post.objects.get(id = pk)
            if request.method == 'POST':            #take it serriously copy this accourtly
                form = NewPostForm(request.POST,request.FILES,instance= up_post)
                form.instance.post_author = request.user
                if form.is_valid():
                    form.save()
                    return redirect(reverse('post',args=(pk,)))
            else:
                form = NewPostForm(instance= up_post)
                form.instance.post_author = request.user
        else:
            return HttpResponse('Your are not valid')
        return render(request,'Blog/postupdate.html',{'form':form})
    '''
            # for permession in class based view PermissionRequiredMixin,
class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
        # this class take default post_confirm_delete.html
        # template_name = 'Blog/post_delete.html'   # it depends on your wish
    success_url = '../'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.post_author:
            return True
        return False

        '''def postdelete(request,pk):
    a = Post.objects.get(id = pk) 
   
    if request.user == a.post_author:
        
        a.delete()
        return redirect('home')
    else:
        return HttpResponse('Your are not valid')    
    # return render(request,'Blog/post_delete.html') '''
#

def subcoment(request): 

    if request.method == 'POST':
        c_form = ComentForm(request.POST)
        postid = Post.objects.get(id = request.POST['postid'])
    
        if c_form.is_valid():
           
            c_form.instance.coment_author = request.user
            c_form.instance.postid = postid
            coment = c_form.save(commit=False)
           
            c_form.save() 
            com = Coment.objects.get(id = coment.pk)
            coment_data =c_form.cleaned_data.get('coment_detail')
            com_auth = com.coment_author
            com_date = com.coment_date
            profile = Profile.objects.get(user=request.user)
            com_auth_img = profile.image.url
            return JsonResponse({'coment':str(coment_data),'author':str(com_auth),'date':com_date,'image':com_auth_img})
    

from django.db.models import Q
def search(request):
    postlist = Post.objects.all()
    query = request.GET['query']
    queryset = postlist.filter(
        Q(post_title__icontains=query)|
        Q(post_detail__icontains=query)
    )
    return render(request,'Blog/search.html',{'queryset':queryset,'query':query})

from django.db.models import Count
def friend_count():
    queryset = Profile.objects.values('user_friend__username').annotate(Count('user_friend__username'))
    return queryset

def user_friendlist(request):
    cu_user = User.objects.get(username=request.user)
    cu_friend_profile =cu_user.profile.user_friend.all()
    return cu_friend_profile

def vote(request):
    select_post = Post.objects.get(id = request.POST['postid'])
    liked = select_post.post_like.all()
    liker_name = User.objects.get(id= request.POST['userid'])
    if liker_name in liked:
        select_post.post_like.remove(request.POST['userid'])
    else:
        select_post.post_like.add(request.POST['userid'])
    result = select_post.post_like.all().count()  
    return redirect(request.META.get('HTTP_REFERER'))


def addfriends(request):
    # grabe user & friend profile
    friend = Profile.objects.get(user= request.POST['friend'])
    user = Profile.objects.get(user = request.POST['user'])

    # now adding friend of both profile
    if user not in friend.user_friend.all():
        friend.user_friend.add(request.POST['user'])
    if friend not in user.user_friend.all():
        user.user_friend.add(request.POST['friend'])
    
    messages.info(request,'You are now friend' )

    # this is for use reverse args function    
    # arg = User.objects.get(id = request.POST['friend'])
    # return redirect(reverse('authorpost',args=(arg,)))
    return redirect(request.META.get('HTTP_REFERER'))   # it is use for same page.

def requestfriend(request):
    print(request.user)
    receiver = Profile.objects.get(user = request.POST['friend'])
    if request.user != receiver.user:
        receiver.friend_req.add(request.user)
        messages.info(request,'Request sended')
    else:
        messages.info(request,'Your are already friend')
    return redirect(request.META.get('HTTP_REFERER'))

def removefriend(request):
    user = Profile.objects.get(user=request.user)
    friend = Profile.objects.get(user__id= request.POST['friend'])
    user.user_friend.remove(request.POST['friend'])
    messages.info(request,f'{friend.user.username} remove from your Friend list' )
    return redirect(request.META.get('HTTP_REFERER'))


def register(request):
    if request.method == 'POST':
        form = Userregister(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)            
            user.is_active = False
            
            form.save()
            current_site = get_current_site(request).domain
            email_sub = 'Activete your Account'
            temp = render_to_string('Blog/email_template.html',
                {'name': user,
                'domain':get_current_site(request).domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':token_generator.make_token(user)})
            Email = EmailMessage(
                email_sub,temp, settings.EMAIL_HOST_USER  ,[user.email]
            )
            Email.send()
            return HttpResponse('An email has been sent in your email pls check this for activate your account')
    else:
        form = Userregister()      
    return render(request,'Blog/register.html',{'form': form})


def activate(request,uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id = uid)
    except:
        user = None
    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('login')
    else:
        return HttpResponse('You are not valid')

@login_required
def profile(request):
    
    friends = []
    for friend in user_friendlist(request):
        friends.append(friend.username)
    
    all_profile = []
    for profile in Profile.objects.all():
        all_profile.append(profile.user.username)
   

    friend_invite = [profile for profile in all_profile if profile not in friends ]
    
    profile = Profile.objects.filter(user__username__in=friend_invite)  
   
    user = Profile.objects.get(user = request.user)
    req = user.friend_req.all().exclude(username__in=friends)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                            request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form':u_form,
        'p_form':p_form,
        'friend_list':user_friendlist(request),
        'other_profile':profile,
        'req': req
    }
    return render(request,'Blog/profile.html',context)



def comentdelete(request,pk):  
    try:
        post = Post.objects.get(id = pk)
        sel_coment = post.coment_set.get(coment_author = request.POST['delete'] )
        sel_coment.delete()
        return redirect(reverse('post',args=(pk,)))
    except:
        return HttpResponse('You have no coment')        
    

   
                
                # this work for newpost useing class
                    #  from django.views import View               
                    # class NewPost(View):
                        
                    #     def get(self, request, *args, **kwargs):
                            
                    #         form = NewPostForm(request.POST,request.FILES)
                            
                    #         if form.is_valid():
                    #             form.save()
                    #             return redirect('blog')
                    #         return render(request,'Blog/post_form.html',{'form':form})

                    #     def post(self, request, *args, **kwargs):
                    #         form = NewPostForm(request.POST,request.FILES)
                    #         form.instance.post_author = self.request.user
                    #         if form.is_valid():
                    #             form.save()
                    #             return HttpResponseRedirect('/blog/')
                            
                    #         return render(request,'Blog/post_form.html',{'form':form})
