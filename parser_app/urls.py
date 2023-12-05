"""resume_parser.parser_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', views.file_upload2, name='file_upload2'),
    path('', views.homepage, name='homepage'),
    path('export_excel',views.export_excel,name = 'export-excel'),
    path('resume_edit/<int:id>',views.resume_edit,name = 'resume-edit'),
    path('api/v1/file_upload_view',views.file_upload_view,name = 'resume-upload'),
    path('api/v1/test',views.test,name = 'test'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
