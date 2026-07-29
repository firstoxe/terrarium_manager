from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .serializers import AnimalViewSet, ActionViewSet, FeedingLogViewSet

router = DefaultRouter()
router.register('animals', AnimalViewSet, basename='api-animal')
router.register('actions', ActionViewSet, basename='api-action')
router.register('feeding', FeedingLogViewSet, basename='api-feeding')

urlpatterns = [
    path('', include(router.urls)),
]
