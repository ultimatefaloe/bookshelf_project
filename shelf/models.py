from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Book(models.Model):
    STATUS_CHOICES = [
        ("want", "Want to Read"),
        ("reading", "Currently Reading"),
        ("read", "Finished"),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="books")
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    cover = models.ImageField(upload_to="book_covers/", blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="want")
    isbn_number = models.CharField(max_length=13, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title[:50]

    def get_absolute_url(self):
        return reverse("book_detail", kwargs={"pk": self.pk})