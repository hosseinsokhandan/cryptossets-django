from django.contrib import admin
from django.urls import path
from account.views import coinex, kucoin, profile
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from authentication.views import signup


urlpatterns = [
    path('', TemplateView.as_view(template_name='exchanges.html'), name="signup"),
    path('signup/', signup, name="signup"),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('coinex/', coinex, name="coinex"),
    path('kucoin/', kucoin, name="kucoin"),
    path('profile/', profile, name="profile"),
]
