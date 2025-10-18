from django.contrib import admin
from .models import GalleryImage, Event, EventImage ,BlogPost,Comment ,HeroSection
from .models import SiteSettings

class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 1  # show one empty slot by default



@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "active", "youtube_url")
    list_editable = ("active",)
    search_fields = ("title",) 

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

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'featured')
    list_filter = ('created_at', 'featured')
    search_fields = ('title', 'content')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'message')

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("site_name", "email", "phone_number")
    fieldsets = (
        ("General Info", {
            "fields": ("site_name", "footer_about")
        }),
        ("Contact Information", {
            "fields": ("phone_number", "email", "address")
        }),
        ("Social Media Links", {
            "fields": ("facebook", "twitter", "instagram", "youtube")
        }),
        ("Footer Text", {
            "fields": ("footer_text",)
        }),
    )

    def has_add_permission(self, request):
        # Prevent multiple entries — only one settings object
        if SiteSettings.objects.exists():
            return False
        return True
   