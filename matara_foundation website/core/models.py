from django.db import models

# Create your models here.
class Gallery(models.Model):
    Tittle =  models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    description = models.TextField()
    date_uploaded = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.Tittle  