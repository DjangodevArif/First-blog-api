from rest_framework import serializers
from Blog.models import Post
from django.contrib.auth.models import User

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            'pk',
            'post_author',
            'post_img',
            'post_title',
            'post_detail',
            'post_date',
            'post_like',
        )
'''
class PostSerializer(serializers.Serializer):
    
    pk = serializers.ReadOnlyField(source ='Arif')
    post_author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    # post_author = serializers.ReadOnlyField()
    post_img = serializers.ImageField()
    post_title = serializers.CharField()
    post_detail = serializers.CharField()
    post_date = serializers.DateTimeField()
    post_like = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),many=True)


    pk = serializers.IntegerField(label='ID', read_only=True)
    post_author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    post_img = serializers.ImageField(max_length=100, required=False)
    post_title = serializers.CharField(max_length=250)
    post_detail = serializers.CharField(max_length=1000, style={'base_template': 'textarea.html'})
    post_date = serializers.DateTimeField(required=False)
    post_like = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False)

'''