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
from website.views import Homepage, RegisterView, AboutusView, ContactusView, CooperationView, logoutView, PostDetailViewCombine, send_request, verify, postsViewByCategories, search, ProfileView
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  
    url(r'^register/', RegisterView.as_view(), name='registerUrl'),
    url(r'^posts/(?P<slug>[\w-]+)/$', PostDetailViewCombine.as_view(),name='postsUrl'),
    url(r'^$', Homepage.as_view(), name='homepageUrl'),
    url(r'^aboutus/', AboutusView.as_view(), name='aboutusUrl'),
    url(r'^contactus/', ContactusView, name='contactusUrl'),
    url(r'^cooperation/', CooperationView, name='cooperationUrl'),
    url(r'^login/$', LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/', logoutView, name='logoutUrl'),
    url(r'^request/$', send_request, name='request'),
    url(r'^verify/$', verify, name='verify'),
    url(r'^postsList/(?P<category_name>\D+)/$', postsViewByCategories.as_view(),name='postsByCategoriesUrl'),
    url(r'^search/$', search.as_view(), name='search'),
    url(r'^accounts/profile/$', ProfileView.as_view(), name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()