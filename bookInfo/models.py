import uuid
from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class Book(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
        )
    
    title = models.CharField(max_length = 200)
    author = models.CharField(max_length = 100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    year_published = models.IntegerField()
    lnaguage = models.CharField(max_length = 50)
    category = models.CharField(max_length = 100)
    
    source_of_collection = models.CharField(max_length = 200)
    book_number = models.CharField(max_length = 50, unique=True)
    shelf_location = models.CharField(max_length = 100)
    is_available = models.BooleanField(default=True)
    num_of_copies = models.IntegerField(default=1)
    num_of_time_borrowed = models.IntegerField(default=0)   
    last_borrowed_date = models.DateTimeField(null=True, blank=True)
    
    
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    
    def get_absolute_url(self):
        return reverse("book_detail", args=[str(self.id)])
        # book_detail is the name of url
        
