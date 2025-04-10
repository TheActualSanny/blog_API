from .models import BlogPost, Comments
from .permissions import CreateIfAuthenticated
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from utils.get_post import get_blog_post
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import PostSerializer, CommentSerializer, PostDetailSerializer
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveAPIView


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
    serializer_class = PostSerializer
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
    serializer_class = CommentSerializer
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
    serializer_class = PostDetailSerializer

        
class LikeEndpoint(APIView):
    
    permission_classes = [CreateIfAuthenticated]
    def post(self, request, pk):
        post_instance = get_blog_post(pk = pk)
        if isinstance(post_instance, Response):
            return post_instance
        post_instance.like_amount += 1
        post_instance.save()
        return Response({
            'message' : 'Successfully liked the post!'
        })

class DislikeEndpoint(APIView):
    def post(self, request, pk):
        post_instance = get_blog_post(pk = pk)
        if isinstance(post_instance, Response):
            return post_instance
        post_instance.dislike_amount += 1
        post_instance.save()
        return Response({
            'message' : 'Successfully disliked the post!'
        })
