from django.db import models
from django.contrib.auth.models import User


class BlogPost(models.Model):
    id = models.AutoField(primary_key = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)
    post_title = models.CharField(max_length = 50)
    post_content = models.TextField()
    like_amount = models.IntegerField(default = 0)
    dislike_amount = models.IntegerField(default = 0)
    date_created = models.DateTimeField(auto_now_add = True)

class Comments(models.Model):
    '''
        This will have 2 foreign keys. so that the client
        can fetch database entries based on either the Users, or the
        Posts.
    '''
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete = models.CASCADE, null = True,
                             blank = True, related_name = 'post_comments')
    comment_content = models.TextField()
    date_created = models.DateTimeField(auto_now_add = True)
