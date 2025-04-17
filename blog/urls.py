from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Blog API",
      default_version='v1',
      description="DRF API offering Blog functionality"
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)



initial_endpoint = 'api/v1'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(initial_endpoint, schema_view.with_ui('swagger'), name = 'documentation'),
    path(f'{initial_endpoint}/blog/', include('blogs.urls')),
    path(f'{initial_endpoint}/authenticate/', include('authentication.urls'))
]
