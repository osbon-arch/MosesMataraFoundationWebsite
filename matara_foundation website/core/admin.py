from django.contrib import admin
from .models import GalleryImage, Event, EventImage

class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 1  # show one empty slot by default


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'uploaded_at')
    list_filter = ('date',)
    search_fields = ('title', 'description')
    inlines = [EventImageInline]


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')


@admin.register(EventImage)
class EventImageAdmin(admin.ModelAdmin):
    list_display = ('event', 'uploaded_at')
