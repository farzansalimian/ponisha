"""ponisha URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.conf import settings
from website.views import Homepage, RegisterView, PostView, AboutusView, ContactusView, CooperationView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  
    url(r'^register/', RegisterView.as_view(), name='registerUrl'),
    url(r'^login/', RegisterView.as_view(), name='loginUrl'),
    url(r'^posts/(?P<slug>[\w-]+)/$', PostView.as_view(),name='postsUrl'),
    url(r'^$', Homepage.as_view(), name='homepageUrl'),
    url(r'^aboutus/', AboutusView.as_view(), name='aboutusUrl'),
    url(r'^contactus/', ContactusView, name='contactusViewUrl'),
    url(r'^cooperation/', CooperationView, name='cooperationViewUrl'),


    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()