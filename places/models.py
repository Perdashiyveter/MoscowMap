from django.db import models
from ckeditor.fields import RichTextField


# Create your models here.
class Place(models.Model):
    name = models.CharField("Название", max_length=255)
    description_short = models.TextField("Краткое описание", blank=True, null=True)
    description_long = RichTextField("Длинное описание", blank=True, null=True)
    latitude = models.FloatField("Широта")
    longitude = models.FloatField("Долгота")

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"

    def __str__(self):
        return self.name


class PlaceImage(models.Model):
    place = models.ForeignKey(Place, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='places_images/')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Картинка места"
        verbose_name_plural = "Картинки места"

    def __str__(self):
        return f"Картинка для {self.place.name}"