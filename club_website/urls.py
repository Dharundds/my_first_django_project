from django import contrib, urls
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('events.urls')),
    path('members/',include('django.contrib.auth.urls')),
    path('members/',include('members.urls')),
]
#config admin titles
admin.site.site_header = 'My Club Administrator Page'
admin.site.site_title = 'Browser Title'
admin.site.index_title ='Welcome to admin area'