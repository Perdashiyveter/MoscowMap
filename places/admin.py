from django.contrib import admin
from .models import Place, PlaceImage
from django.utils.html import format_html
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase


class PlaceImageInLine(SortableInlineAdminMixin, admin.TabularInline):
    model = PlaceImage
    extra = 1
    fields = ('image', 'preview')
    readonly_fields = ('preview',)
    ordering = ('order',)

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:150px; width:auto; object-fit:contain;" />',
                obj.image.url
            )
        return ""


# Register your models here.
@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name','description_short','description_long', )
    fieldsets = (
        (None, {'fields': ('name', 'description_short', 'description_long')}),
        ('Местоположение', {'fields': ('latitude', 'longitude')}),
    )

    inlines = [PlaceImageInLine]