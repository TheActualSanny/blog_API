from django.db import models
from django.contrib.auth.models import User

class FeedbackSystem(models.Model):
    '''
        The structure for Like/Dislike models.
        Considering that this is an interface and not
        a model to be instantiated, it is implemented
        in a seperate module.
    '''
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    post = models.ForeignKey('blogs.BlogPost', on_delete = models.CASCADE,
                             null = True, blank = True)

    class Meta:
        abstract = True
        app_label = 'blogs'