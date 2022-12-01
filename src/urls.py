from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from users import views as users_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('cards.urls')),
    
    path("register/", users_views.register, name="register"),

    path("__reload__/", include("django_browser_reload.urls"))
] 

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
