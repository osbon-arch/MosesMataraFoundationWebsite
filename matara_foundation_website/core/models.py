from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from embed_video.fields import EmbedVideoField
from ckeditor_uploader.fields import RichTextUploadingField


class HeroSection(models.Model):
    title = models.CharField(max_length=200, help_text="Main headline text")
    subtitle = models.CharField(max_length=300, blank=True, help_text="Optional subheading")
    image = models.ImageField(upload_to='hero/', blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True, help_text="YouTube video link (optional)")
    button_text = models.CharField(max_length=50, blank=True, null=True)
    button_link = models.URLField(blank=True, null=True)
    active = models.BooleanField(default=True, help_text="Only one hero section should be active at a time")

    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Sections"

    def __str__(self):
        return self.title

    def embed_video_id(self):
        """Extract the YouTube video ID."""
        import re
        if not self.youtube_url:
            return None
        match = re.search(r"(?:v=|be/)([A-Za-z0-9_-]{11})", self.youtube_url)
        return match.group(1) if match else None


class GalleryImage(models.Model):
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='gallery/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title or f"Image {self.id}"


# --- EVENT MODEL---
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.title} ({self.date.year})"


class EventImage(models.Model):
    event = models.ForeignKey(Event, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    caption = models.CharField(max_length=150, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.event.title} - Image {self.id}"

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    video = EmbedVideoField(blank=True, null=True)  # Optional video field
    author = models.CharField(max_length=100, default="Matara Moses Foundation")
    content = RichTextUploadingField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("blog_detail", kwargs={"slug": self.slug})

class Comment(models.Model):
    post = models.ForeignKey('BlogPost', related_name='comments', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.name}"

    def children(self):
        return self.replies.all()

    def is_parent(self):
        return self.parent is None

# models.py
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"


class SiteSettings(models.Model):
    # General
    site_name = models.CharField(max_length=150, default="Matara Moses Foundation")
    footer_about = models.TextField(
        default="The Matara Moses Foundation is dedicated to transforming lives through education. We provide access, mentorship, and resources for children across Kenya to achieve their dreams."
    )

    # Contact info
    phone_number = models.CharField(max_length=30, default="+254 712 345 678")
    email = models.EmailField(default="info@mataramosesfoundation.org")
    address = models.CharField(max_length=255, default="Mombasa, Kenya")

    # Social media links
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)

    # Footer
    footer_text = models.CharField(max_length=255, default="© 2025 Matara Moses Foundation | Built with ❤️ for a brighter tomorrow")

    def __str__(self):
        return "Site Settings"

    class Meta:
        verbose_name_plural = "Site Settings"
