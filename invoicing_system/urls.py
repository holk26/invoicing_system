from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView, LoginView
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    
    # Reemplazar la inclusión estándar de auth urls con rutas específicas
    # para evitar conflicto con la ruta de logout personalizada
    path('accounts/login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    
    # Configurar explícitamente la ruta de logout en accounts/logout/ y permitir método GET
    path('accounts/logout/', LogoutView.as_view(next_page='/', http_method_names=['get', 'post']), name='logout'),
]