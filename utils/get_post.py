from blogs.models import BlogPost
from rest_framework.response import Response

def get_blog_post(pk: int) -> BlogPost | None:
    try:
        post_instance = BlogPost.objects.get(pk = pk)
    except BlogPost.DoesNotExist:
        return Response({
            'detail' : 'Make sure to pass a correct id!'
        })
    return post_instance