from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Application
from .forms import ApplicationForm

def apply(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('apply')
    else:
        form = ApplicationForm()

    return render(request, 'applications/apply.html', {'form': form})


def check_status(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone_number')

        try:
            app = Application.objects.get(email=email, phone_number=phone)
            context['application'] = app
        except Application.DoesNotExist:
            messages.error(request, "No application found. Please check your details.")
    return render(request, 'applications/check_status.html', context)
