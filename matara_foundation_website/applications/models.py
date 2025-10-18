from django.db import models

# Create your models here.
from django.db import models

class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    county = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    application_file = models.FileField(upload_to='applications/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.status}"



# applications/models.py

from django.db import models

class SponsoredChild(models.Model):
    full_name = models.CharField(max_length=200)
    guardian_name = models.CharField(max_length=200)
    current_school = models.CharField(max_length=200)
    school_contact_person = models.CharField(max_length=200)
    guardian_phone = models.CharField(max_length=15)
    school_contact_phone = models.CharField(max_length=15)
    county = models.CharField(max_length=100, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return self.full_name


class AcademicReport(models.Model):
    TERM_CHOICES = [
        ('Term 1', 'Term 1'),
        ('Term 2', 'Term 2'),
        ('Term 3', 'Term 3'),
    ]
    child = models.ForeignKey(SponsoredChild, related_name='reports', on_delete=models.CASCADE)
    term = models.CharField(max_length=20, choices=TERM_CHOICES)
    year = models.PositiveIntegerField()
    file = models.FileField(upload_to='academic_reports/')
    average_grade = models.CharField(max_length=5, blank=True, null=True)
    remarks = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-year', '-term']

    def __str__(self):
        return f"{self.child.full_name} - {self.term} {self.year}"
