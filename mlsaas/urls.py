
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static

# TODO : Set correct robots.txt & sitemap
from django.http import HttpResponse
from rest_framework_jwt.views import obtain_jwt_token
from django.views.generic import TemplateView
from web import settings

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^google37306863f3b606bc.html$',TemplateView.as_view(template_name='google37306863f3b606bc.html')),
    url(r'^robots.txt$', lambda r: HttpResponse("User-agent: *\nAllow: /", content_type="text/plain")),
    url(r'^api-token-auth/', obtain_jwt_token),

    url(r'^scan/', include('scan.urls')),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^', include('django_evercookie.urls')),
    url(r'^', include('portal.urls')),
]
# Serve media like categories picture
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
