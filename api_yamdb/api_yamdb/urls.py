from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from core import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('import/', views.data_import),
    path('api/', include('api.urls')),
    path('api/v1/', include('users.urls')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('api/', include('users.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    # Добавить к списку urlpatterns список адресов из приложения debug_toolbar:
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
