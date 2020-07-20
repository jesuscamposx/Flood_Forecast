from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api.views_integration import CargaCondicionView, CargaInundacionView
from api.views_integration import CargaCondicionLPView, CargaCallesView
from api.views_files import ArchivoInundacionView, ArchivoNivelView
from api.views_files import CatInundacion, CatMedicion
from api.views_ml import ConjuntosView, PrediccionView
from api.views_network import SensorView, MedicionView, UltMedicionView
from api.views_locations import CalleView, ColoniaView, AlcaldiaView
from api.views_alerts import DestinatarioView
from api.views_extra import EmailView

urlpatterns = [
    path('carga/condicion', CargaCondicionView.as_view()),
    path('carga/condicionlp', CargaCondicionLPView.as_view()),
    path('carga/inundacion', CargaInundacionView.as_view()),
    path('carga/calle', CargaCallesView.as_view()),
    path('ml/conjuntos', ConjuntosView.as_view()),
    path('ml/prediccion', PrediccionView.as_view()),
    path('archivo/inundacion', ArchivoInundacionView.as_view()),
    path('archivo/inundacion/catalogo', CatInundacion.as_view()),
    path('archivo/nivel-agua', ArchivoNivelView.as_view()),
    path('archivo/nivel-agua/catalogo', CatMedicion.as_view()),
    path('sensor', SensorView.as_view()),
    path('medicion', MedicionView.as_view()),
    path('medicion/ultima', UltMedicionView.as_view()),
    path('alerta', DestinatarioView.as_view()),
    path('calle', CalleView.as_view()),
    path('colonia', ColoniaView.as_view()),
    path('alcaldia', AlcaldiaView.as_view()),
    path('email', EmailView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
