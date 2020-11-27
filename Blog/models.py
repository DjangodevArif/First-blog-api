from django.db import models

import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
from django.core.exceptions import ValidationError
# Create your models here.

# to custome image save file
from django.core.files.images import get_image_dimensions   
def user_img_path(instance,filename):
    return 'profile_pics/{0}/{1}'.format(instance.user,filename)

class Profile(models.Model):

    country_filds =(('Usa','Usa'),('Bangladesh','Bangladesh'),('Qatar','Qatar'),('Dubai','Dubai'),
    ('England','England'),('Sudi Arabia','Sudi Arabia'))

    

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to =user_img_path)
    country = models.CharField(max_length=50,choices=country_filds,default='Bangeldesh')
    user_friend = models.ManyToManyField(User,related_name='friends',blank=True)
    friend_req = models.ManyToManyField(User,related_name='request',blank=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size =(300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)


#>>>>> Post model 

class nothing(models.Model):
    name = models.CharField(max_length=100)

class Post(models.Model):

    post_author = models.ForeignKey(User,on_delete=models.CASCADE)
    post_img = models.ImageField(default='post_pic.jpg',upload_to='post_pics')
    post_title = models.CharField(max_length=250)
    post_detail = models.TextField(max_length=1000)
    post_date = models.DateTimeField(default=timezone.now)
    post_like = models.ManyToManyField(User,related_name='+',blank=True)


    def __str__(self):
        return  f'{self.post_title } and id: { self.id }'

    def recent(self):
        if timezone.now() - datetime.timedelta(days=1)   <= self.post_date <= timezone.now():
            return True




class Coment(models.Model):
    postid = models.ForeignKey(Post,on_delete=models.CASCADE)
    coment_author = models.ForeignKey(User,on_delete=models.CASCADE)
    coment_detail = models.TextField(max_length=150)
    coment_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.postid.post_title} by {self.coment_author.username}'


class Co_coment(models.Model):
    main_coment = models.ForeignKey(Coment,on_delete=models.CASCADE)
    coment_author = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    coment_detail = models.TextField(max_length=150)
    coment_date = models.DateField(auto_now_add=True)
