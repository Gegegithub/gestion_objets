from django.contrib import admin
from django.urls import path, include
from django.views import View
from django.shortcuts import redirect

def redirect_to_login(request):
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_login, name='root'),  # Redirection de la racine vers login
    path('app/', include('monappli.urls')),  # Changement du préfixe pour l'application monappli
    path('auth/', include('authentication.urls')),
]
