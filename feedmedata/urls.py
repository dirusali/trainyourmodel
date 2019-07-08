from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500


# TODO : Set correct robots.txt & sitemap
from django.http import HttpResponse
from rest_framework_jwt.views import obtain_jwt_token
from django.views.generic import TemplateView
from web import settings
from django.contrib.sitemaps.views import sitemap
from portal.sitemaps import SearchTagSitemap, CategorySitemap, SearchTagSitemapFemale, StaticViewSitemap
from portal import views as portal_views

sitemaps = {
    'tags': SearchTagSitemap,
    'femaletags': SearchTagSitemapFemale,
    'categories': CategorySitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    url(r'^', include('portal.urls')),    
    url(r'^admin/', admin.site.urls),
    url(r'^google37306863f3b606bc.html$',TemplateView.as_view(template_name='google37306863f3b606bc.html')),
    #url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^scan/', include('scan.urls')),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^', include('django_evercookie.urls')),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
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
