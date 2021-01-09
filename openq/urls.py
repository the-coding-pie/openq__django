from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from quiz import views
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quiz.urls')),
]

handler404 = views.handler404
handler500 = views.handler500

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)