from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

from users import views as users_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('cards.urls')),
    
    path("sign-in/", users_views.register, name="sign-in"),
    path("login/", users_views.Login.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="users/logout.html"), name="logout"),
    path("profile/", users_views.profile, name="profile"),

    path("__reload__/", include("django_browser_reload.urls"))
] 

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
