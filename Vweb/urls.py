"""
URL configuration for Vweb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from django.urls import include

from web import views as views_web

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    path('', views_web.origin),
    path('core', views_web.core),
    path('data', views_web.data),
    path('code', views_web.code),
    path('visual', views_web.visual),
    path('report', views_web.report),

    path('test/catalog', views_web.test_catalog),
    path('test/codes', views_web.test_code_simu_refresh),
    path('test/codev', views_web.test_code_visu_refresh),
    path('test/data', views_web.test_data_list_refresh),

    path("django_plotly_dash/", include("django_plotly_dash.urls")),

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)