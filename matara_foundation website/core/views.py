from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from .models import GalleryImage ,Event ,EventImage ,BlogPost ,Comment
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect

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

def blog(request):
    year_filter = request.GET.get('year')

    if year_filter:
        posts = BlogPost.objects.filter(created_at__year=year_filter).order_by('-created_at')
    else:
        posts = BlogPost.objects.all()

    years = BlogPost.objects.dates('created_at', 'year', order='DESC')

    return render(request, "core/blog.html", {
        "posts": posts,
        "years": years,
    })
#Blog View
def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    comments = Comment.objects.filter(post=post, parent__isnull=True)

    if request.method == "POST":
        name = request.POST.get("name")
        message = request.POST.get("message")
        parent_id = request.POST.get("parent_id")

        if name and message:
            parent_comment = Comment.objects.get(id=parent_id) if parent_id else None
            Comment.objects.create(post=post, name=name, message=message, parent=parent_comment)

        return redirect(post.get_absolute_url())

    return render(request, "core/blog_detail.html", {
        "post": post,
        "comments": comments
    })