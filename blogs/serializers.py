from rest_framework import serializers
from .models import BlogPost, Comments

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.username')
    blog_title = serializers.CharField(source = 'post.post_title')
    
    class Meta:
        model = Comments
        fields = ['user', 'blog_title', 'comment_content', 'date_created']
        
class PostSerializer(serializers.ModelSerializer):
    '''
        Serializer which we use to list/create BlogPost instances.
        The class has a create() method implemented by default, which will handle the POST calls to
        the endpoint.

        Instead of passing a user directly, it will be set in the perform_create() method inside
        the view.
    '''
    user = serializers.ReadOnlyField(source = 'user.username')
    class Meta:
        model = BlogPost
        fields = ['id', 'user', 'post_title', 'post_content']

class PostDetailSerializer(serializers.ModelSerializer):
    '''
        For the generic PostEndpoint View, we use
        PostSerializer, which includes less fields.

        This serializer class will be used in the PostDetailedEndpoint view. 
    '''
    user = serializers.ReadOnlyField(source = 'user.username')
    post_comments = CommentSerializer(many = True, read_only = True)
    
    class Meta:
        model = BlogPost
        fields = ['user', 'post_title', 'post_content', 'date_created', 'post_comments',
                  'like_amount', 'dislike_amount']