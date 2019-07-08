from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500


# TODO : Set correct robots.txt & sitemap
from django.http import HttpResponse
#from rest_framework_jwt.views import obtain_jwt_token
from django.views.generic import TemplateView
from feedmedata import settings
from django.contrib.sitemaps.views import sitemap
#from portal.sitemaps import SearchTagSitemap, CategorySitemap, SearchTagSitemapFemale, StaticViewSitemap
from portal import views as portal_views



urlpatterns = [
    url(r'^', include('portal.urls')),    
    url(r'^admin/', admin.site.urls),
    #url(r'^api-token-auth/', obtain_jwt_token),
]
# Serve media like categories picture
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

handler404 = portal_views.error404
handler500 = portal_views.error500   
