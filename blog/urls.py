from django.contrib import admin
from django.urls import path, include

initial_endpoint = 'api/v1'

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls')),
    path(f'{initial_endpoint}/blog/', include('blogs.urls')),
    path(f'{initial_endpoint}/authenticate/', include('authentication.urls'))
]
