import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.urls import reverse


# ----------------------------------------------------------
# 1️⃣ Book 
# ----------------------------------------------------------
class Book(models.Model):
    id = models.UUIDField(primary_key=True, 
                        default=uuid.uuid4, 
                        editable=False)
    
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    cover = models.ImageField(upload_to="covers/", blank=True)

    year_published = models.IntegerField()
    language = models.CharField(max_length=50)
    category = models.CharField(max_length=100)

    source_of_collection = models.CharField(max_length=200)
    book_number = models.CharField(max_length=50, unique=True)
    shelf_location = models.CharField(max_length=100)

    is_available = models.BooleanField(default=False)
    num_of_copies = models.IntegerField(default=1)
    num_of_time_borrowed = models.IntegerField(default=0)
    last_borrowed_date = models.DateTimeField(null=True, blank=True)
    
    class Meta: # new
        permissions = [
        ("special_status", "Can read all books"),
        ]

    def save(self, *args, **kwargs):
        self.is_available = self.num_of_copies > 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} by {self.author}"

    def get_absolute_url(self):
        return reverse("book_detail", args=[str(self.id)])


# ----------------------------------------------------------
# 2 Review
# ----------------------------------------------------------
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    review = models.TextField(max_length=500)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Review by {self.author} on {self.book.title}"

    def get_absolute_url(self):
        return reverse("book_detail", kwargs={"pk": self.book.pk})


# ----------------------------------------------------------
# Search item
# ----------------------------------------------------------
