from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'book.views.home', name='home'),
    url(r'^export_xls$', 'book.views.export_xls', name='export_xls'),
    url(r'^export/(?P<format>[a-z]+)$', 'book.views.export_books', name='export'),
    url(r'^import/(?P<format>[a-z]+)$', 'book.views.import_books', name='import'),
    # url(r'^django_import_example/', include('django_import_example.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
