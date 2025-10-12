from django.shortcuts import render

from core.models import Gallery

# Create your views here.
def home(request):
    return render(request, "core/home.html")

def Gallery_view(request):
    Gallery_images = Gallery.objects.all()
    context = { 'Gallery_images': Gallery_images }

    return render(request, "core/gallery.html", context)

