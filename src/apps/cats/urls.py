from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.cats.views import (
    BreedsListView,
    CatsViewSet,
    CatRatingView
)

router = DefaultRouter()
router.register(r'', CatsViewSet, basename='cats')

urlpatterns = [
    path('v1/', include(router.urls)),
    path("breeds/", BreedsListView.as_view()),
    path("rating/", CatRatingView.as_view())
]
