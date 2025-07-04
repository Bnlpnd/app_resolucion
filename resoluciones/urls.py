from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('registro/', views.registro, name='registro'),
    path('resoluciones/', views.ResolucionListView.as_view(), name='lista_resoluciones'),
    path('resoluciones/<int:pk>/', views.ResolucionDetailView.as_view(), name='detalle_resolucion'),
    path('resoluciones/nueva/', views.crear_resolucion, name='crear_resolucion'),
    path('resoluciones/<int:pk>/editar/', views.editar_resolucion, name='editar_resolucion'),
    path('mis-resoluciones/', views.mis_resoluciones, name='mis_resoluciones'),
] 