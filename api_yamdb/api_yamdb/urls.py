from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('import/', views.data_import),
    path('api/', include('api.urls')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
