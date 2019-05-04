# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path
from django.utils.decorators import method_decorator
from allauth.account.views import LoginView
from axes.decorators import axes_dispatch
from axes.decorators import axes_form_invalid
from activities.sitemap import ActivitySitemap
from users.forms import LoginForm

admin.autodiscover()

LoginView.dispatch = method_decorator(axes_dispatch)(LoginView.dispatch)
LoginView.form_invalid = method_decorator(axes_form_invalid)(LoginView.form_invalid)

urlpatterns = [
    url(r'^admin/', admin.site.urls),  # NOQA
    url(r'^favorites/', include('favorites.urls')),
    url(r'^reviews/', include('reviews.urls')),
    url(r'^moderations/', include('moderations.urls')),
    url(r'^accounts/login/', LoginView.as_view(form_class=LoginForm), name='account_login'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^', include('users.urls')),
    url(r'^', include('cms.urls')),
]

urlpatterns += [
    path('sitemap.xml', sitemap, {
        'sitemaps': {
            'cmspages': CMSSitemap,
            'activities': ActivitySitemap,
        }
    }),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
