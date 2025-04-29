from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect
from django.contrib.auth import logout

def custom_logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/logout/', custom_logout_view, name='logout'),
]