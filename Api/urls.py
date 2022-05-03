from django.urls import path, include
from rest_framework import routers
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView
router = routers.DefaultRouter()

router.register("groups", GroupViewSet)
router.register("users", UserViewSet)
router.register('personnel',PersonnelsViewSet,basename='personnel')
router.register('voiture',VoitureViewSet,basename='voiture')
router.register('carburant',CarburantViewSet,basename='carburant')
router.register('etat',EtatViewSet,basename='etat')
router.register('document',DocumentViewSet,basename='document')
router.register('chauffeur',ChauffeurViewSet,basename='chauffeur')
router.register('tarif',TarifViewSet,basename='Tarif')
router.register('location',LocationViewSet,basename='location')


urlpatterns = [
    path('', include(router.urls)),
    path('login/', TokenPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('api_auth', include('rest_framework.urls')),

]