from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('delicious_project.delicious.urls')),
    path('account/', include('delicious_project.accounts.urls')),
    path('recipe/', include('delicious_project.delicious.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
