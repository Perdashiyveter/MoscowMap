import json
from django.core.management.base import BaseCommand
from places.models import Place, PlaceImage
from django.core.files.base import ContentFile
import requests


class Command(BaseCommand):
    help = 'Загружает место по JSON URL или локальному пути'

    def add_arguments(self, parser):
        parser.add_argument('json_url', help='URL или локальный путь к JSON файлу')

    def handle(self, *args, json_url, **options):
        # Загружаем JSON
        if json_url.startswith('http'):
            response = requests.get(json_url)
            response.raise_for_status()
            data = response.json()
        else:
            with open(json_url, encoding='utf-8') as file:
                data = json.load(file)

        # Создаём место
        place, created = Place.objects.get_or_create(
            name=data['title'],
            defaults={
                'description_short': data.get('description_short', ''),
                'description_long': data.get('description_long', ''),
                'latitude': float(data['coordinates']['lat']),
                'longitude': float(data['coordinates']['lng']),
            }
        )

        # Загружаем картинки
        for index, img_url in enumerate(data.get('imgs', [])):
            img_response = requests.get(img_url)
            img_response.raise_for_status()

            image_file = ContentFile(img_response.content)
            filename = img_url.split('/')[-1]

            PlaceImage.objects.create(
                place=place,
                image=filename
            ).image.save(filename, image_file, save=True)

        self.stdout.write(self.style.SUCCESS(f'Загружено место: {place.name}'))