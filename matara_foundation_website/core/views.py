from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from .models import GalleryImage ,Event ,EventImage ,BlogPost ,Comment
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.core.mail import EmailMessage
from django.contrib import messages
from .models import ContactMessage
from .models import HeroSection
from django.contrib.auth.models import User

# Home view
def home(request):
    return render(request, "core/home.html")

def home(request):
    hero = HeroSection.objects.filter(active=True).first()
    return render(request, "core/home.html", {"hero": hero})

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

    # Handle AJAX comment submission
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        name = request.POST.get("name")
        message = request.POST.get("message")
        parent_id = request.POST.get("parent_id")

        if not name or not message:
            return JsonResponse({"error": "Name and message are required."}, status=400)

        parent = Comment.objects.filter(id=parent_id).first() if parent_id else None
        new_comment = Comment.objects.create(post=post, name=name, message=message, parent=parent)

        # Return a small HTML snippet for instant insertion
        html = f"""
        <div class="mt-3 ms-{ '4' if parent else '0' } p-3 bg-white rounded border-start border-warning animate-fade-in">
            <strong>{new_comment.name}</strong>
            <span class="text-muted small">{new_comment.created_at.strftime("%B %d, %Y, %I:%M %p")}</span>
            <p class="mt-2">{new_comment.message}</p>
        </div>
        """
        return JsonResponse({"html": html})

    return render(request, "core/blog_detail.html", {
        "post": post,
        "comments": comments
    })

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Save to database
        ContactMessage.objects.create(name=name, email=email, message=message)

        # Send email
        email_subject = f"New Message from {name}"
        email_body = f"From: {name} <{email}>\n\n{message}"

        email_message = EmailMessage(email_subject, email_body, to=["yourgmail@gmail.com"])
        email_message.send()

        messages.success(request, "Your message has been sent successfully!")
        return redirect("contact")

    return render(request, "core/contact.html")

def create_admin(request):
    if User.objects.filter(username="admin").exists():
        return HttpResponse("Admin user already exists")
    User.objects.create_superuser("admin", "admin@example.com", "AdminPass123")
    return HttpResponse("Superuser created successfully!")