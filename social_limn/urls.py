"""social_limn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from rest_framework import routers
from core import views
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

# Use automatic URL routing for API
# Include login URLS for browsable API

"""
Django's default login/logout as well as password management urls and views
are included under 'accounts/', as we create templates/react for user changing
password, we'll need to reference the Django docs for those urls and views.

The signup url is set up in the project rather than in core because it is "outside"
of our authenticated app-level urls. This structure worked best for redirecting
between login/logout and signup.
"""
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include(router.urls)),
    path('', views.home, name='home'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('limn/', include('core.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.signup, name='signup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)