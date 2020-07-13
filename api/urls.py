from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api.views_integration import CargaCondicionView, CargaInundacionView
from api.views_files import ArchivoView
from api.views_ml import ConjuntosView
from api.views_network import SensorView, MedicionView
from api.views_locations import CalleView
from api.views_alerts import DestinatarioView

urlpatterns = [
    path('carga/condicion', CargaCondicionView.as_view()),
    path('carga/inundacion', CargaInundacionView.as_view()),
    path('ml/conjuntos', ConjuntosView.as_view()),
    path('archivo', ArchivoView.as_view()),
    path('sensor', SensorView.as_view()),
    path('medicion', MedicionView.as_view()),
    path('alerta', DestinatarioView.as_view()),
    path('calle', CalleView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
