"""
URL configuration for crud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('signin_admin/', views.signin_admin, name='signin_admin'),
    path('panel_administrador/', views.panel_administrador, name='panel_administrador'),
    path('publicacionespendientes/', views.publicacionespendientes, name='publicacionespendientes'),
    path('reportes/', views.reportes, name='reportes'),
    path('adminarticulos/', views.adminarticulos, name='adminarticulos'),
    path('admineditarusuarios/<int:id_usuario>/', views.admineditarusuarios, name='admineditarusuarios'),
    path('adminusuarios/', views.adminusuarios, name='adminusuarios'),
    path('adminagregar/', views.adminagregar, name='adminagregar'),
    path('admincategorias/', views.admincategorias, name='admincategorias'),
    path('admincrearcat/', views.admincrearcat, name='admincrearcat'),
    path('admineditarcat/', views.admineditarcat, name='admineditarcat'),
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('datosdeusuario', views.datosdeusuario, name='datosdeusuario'),
    path('logout', views.signout, name='logout'),
    path('signin', views.signin, name='signin'),
    path('perfil', views.perfil, name='perfil'),
    path('editardatos', views.editardatos, name='editardatos'),
    path('nuevoarticulo', views.nuevoarticulo, name='nuevoarticulo'),
    path('paginafavoritos', views.paginafavoritos, name='paginafavoritos'),
    path('publicados', views.publicados, name='publicados'),
    path('<int:pk>/', views.detalle_articulo, name='detalle_articulo'),
    path('editararticulos', views.editararticulos, name='editararticulos'),
    path('reportar', views.reportar, name='reportar'),
    path('buscar/', views.buscar, name='buscar'),
    path('<str:nombre_usuario>/', views.detalle_usuario, name='detalle_usuario'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)