from rest_framework import serializers
from .models import BlogPost, Comments, Like, Dislike

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
    like_amount = serializers.SerializerMethodField()
    dislike_amount = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = ['user', 'post_title', 'post_content', 'date_created', 'post_comments',
                  'like_amount', 'dislike_amount']

    def get_like_amount(self, obj):
        return Like.objects.filter(post = obj).count()

    def get_dislike_amount(self, obj):
        return Dislike.objects.filter(post = obj).count()

class FeedbackSystemSerialier(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.username')
    post = serializers.SlugRelatedField(queryset=BlogPost.objects.all(), slug_field='post_title')

    def create(self, validated_data, model: Like | Dislike):
        '''
            This is an abstract solution to
            handle liking/disliking 

        '''

        user_instance = validated_data.get('user')
        post_instance = validated_data.get('post')

        opposite = Dislike if isinstance(model, Like) else Like
        inst = None

        try:
            opposite_action = opposite.objects.get(post = post_instance, user = user_instance)
            opposite_action.delete()
            inst = model.objects.create(user = user_instance, post = post_instance)

        except opposite.DoesNotExist:
            try:
                action = model.objects.get(post = post_instance, user = user_instance)
                action.delete()
                return action
                
            except model.DoesNotExist:
                inst = model.objects.create(user = user_instance, post = post_instance)
        return inst

    
class LikeSerializer(FeedbackSystemSerialier):
    class Meta:
        model = Like
        fields = ['user', 'post']
    
    def create(self, validated_data):
        return super().create(validated_data, model = Like)
    
class DislikeSerializer(FeedbackSystemSerialier):
    class Meta:
        model = Dislike
        fields = ['user', 'post']

    def create(self, validated_data):
        return super().create(validated_data, model = Dislike)