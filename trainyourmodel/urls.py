from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500
from django.http import HttpResponse
from django.views.generic import TemplateView
from trainyourmodel import settings
from django.contrib.sitemaps.views import sitemap
from portal import views as portal_views



urlpatterns = [
    url(r'^', include('portal.urls')),    
    url(r'^admin/', admin.site.urls),
    url(r'^api-token-auth/', obtain_jwt_token),
]
