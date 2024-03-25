from django.contrib import admin
from django.urls import path, include
from admins import views as admin_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('django_admin/', admin.site.urls),
    
    path('', admin_views.index, name='index'),
    path('about/', admin_views.about, name='about'),
    path('contact/', admin_views.contact, name='contact'),
    path('members/', include('members.urls')),
    path('admin/', include('admins.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
