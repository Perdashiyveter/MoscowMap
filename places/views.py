from django.shortcuts import render
from django.http import Http404, JsonResponse
from .models import Place


# Create your views here.
def index(request):
    return render(request, "index.html")


def place(request, place_id):
    try:
        place = Place.objects.get(id=place_id)
    except Place.DoesNotExist:
        raise Http404("Place not found")

    data = {
        "id": place.id,
        "title": place.name,
        "description_short": place.description_short,
        "description_long": place.description_long,
        "imgs": [img.image.url for img in place.images.all()]
    }

    return JsonResponse(data, json_dumps_params={"ensure_ascii": False})


def places_json(request):
    features = []

    for place in Place.objects.all():
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(place.longitude), float(place.latitude)]
            },
            "properties": {
                "title": place.name,
                "placeId": place.id,
                "detailsUrl": f"/places/{place.id}"
            }
        })

    return JsonResponse({
        "type": "FeatureCollection",
        "features": features
    })