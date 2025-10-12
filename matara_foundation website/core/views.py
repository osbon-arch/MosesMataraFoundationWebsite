from django.shortcuts import render
from .models import GalleryImage ,Event ,EventImage
from django.http import JsonResponse

# Create your views here.
def home(request):
    return render(request, "core/home.html")

def gallery(request):
    year_filter = request.GET.get('year')

    if year_filter:
        events = Event.objects.filter(date__year=year_filter).prefetch_related('images')
    else:
        events = Event.objects.all().prefetch_related('images')

    years = Event.objects.dates('date', 'year', order='DESC')
    images = GalleryImage.objects.all()

    return render(request, "core/gallery.html", {
        "images": images,
        "events": events,
        "years": years
    })

def event_images_api(request, event_id):
    images = EventImage.objects.filter(event_id=event_id)
    data = {"images": [{"url": img.image.url} for img in images]}
    return JsonResponse(data)

def event_images(request, event_id):
    from .models import EventImage
    images = EventImage.objects.filter(event_id=event_id)
    data = {"images": [{"url": i.image.url} for i in images]}
    return JsonResponse(data)
