from .models import BlogPost, Comments, Like, Dislike
from .permissions import CreateIfAuthenticated
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from utils.get_post import get_blog_post
from rest_framework.permissions import AllowAny, IsAuthenticated
from . import serializers
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveAPIView, CreateAPIView


class APIRoot(APIView):
    '''
        The root endpoint. Considering that we don't perform any CRUD operations here,
        we use an APIView instead of generic views.
    '''
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            'blog-posts' : reverse('post-endpoint', request = request),
            'comments' : reverse('comment-endpoint', request = request)
        })
    
class PostEndpoint(ListCreateAPIView):
    '''
        Will handle the listing and the creation of post instances.
        The user column of the table will be determined on creation of 
        an object.
    '''
    queryset = BlogPost.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [CreateIfAuthenticated]

    def perform_create(self, serializer):
        '''
            This will set the current user initially.
            Other data will be passed to the serializer, and create()
            method will be called.

        '''
        serializer.save(user = self.request.user)

class CommentEndpoint(ListCreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [CreateIfAuthenticated]

    def perform_create(self, serializer):
        '''
            We are going to fetch the BlogPost instance and pass that
            directly to the serializer.
            The current user is also being set here.
        '''
        blog_title = self.request.data.get('blog_title')
        try:
            post = BlogPost.objects.get(post_title = blog_title)
        except BlogPost.DoesNotExist:
            return Response({
                'message' : 'Post with the given title doesnt exist!'
            })
        serializer.save(post = post, user = self.request.user)

class PostDetailedEndpoint(RetrieveAPIView):
    '''
        Returns detailed information about a post, such is it's creation date,
        associated comments and like/dislike count.
    '''
    queryset = BlogPost.objects.prefetch_related('post_comments')
    permission_classes = [CreateIfAuthenticated]
    serializer_class = serializers.PostDetailSerializer

        
class LikeEndpoint(CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = serializers.LikeSerializer
    permission_classes = [CreateIfAuthenticated]

    def perform_create(self, serializer):
        blog_title = self.request.data.get('post')
        try:
            post_instance = BlogPost.objects.get(post_title = blog_title)
        except BlogPost.DoesNotExist:
            return Response({
                'message' : 'Make sure to pass a correct post title!'
            })
        serializer.save(user = self.request.user, post = post_instance)

class DislikeEndpoint(CreateAPIView):
    queryset = Dislike.objects.all()
    serializer_class = serializers.DislikeSerializer
    permission_classes = [CreateIfAuthenticated]

    def perform_create(self, serializer):
        blog_title = self.request.data.get('post')
        try:
            post_instance = BlogPost.objects.get(post_title = blog_title)
        except BlogPost.DoesNotExist:
            return Response({
                'message' : 'Make sure to pass a correct post title!'
            })
        serializer.save(user = self.request.user, post = post_instance)