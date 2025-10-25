from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('places/geojson/', views.places_json, name="places_json"),
    path('places/<int:place_id>', views.place, name="place")
]