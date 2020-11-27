from django.shortcuts import render

from Blog.models import *
from api.permissions import IsOwnerOnly

from rest_framework import renderers
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import permissions

from .serializers import PostSerializer 

# Create your views here.

'''   
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
'''

class PostDetail(IsOwnerOnly,generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer



@api_view(['GET','POST'])
def postlist(request):
    
    if request.method == 'GET':
        post = Post.objects.all()
        serializer_class = PostSerializer
        # print(post)
        serializer = PostSerializer(post, many =True)     # manay =True
        print(IsOwnerOnly.has_object_permission)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.data)
            # serializer.save()
            return Response(serializer.data,status=HTTP_201_CREATED)
        return Response(serializer.errors,status=HTTP_404_BAD_REQUEST)

class Apithings(generics.GenericAPIView):

    queryset = Post.objects.all()
    renderer_classes = [ renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        return Response(post.post_author)